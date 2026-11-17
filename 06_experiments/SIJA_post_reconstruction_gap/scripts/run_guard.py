"""Local JSONL runner. Private outputs only. One visible GPU, resumable, no editing."""
import argparse,json,time,hashlib,re,os,subprocess,threading,signal
from pathlib import Path

def parse(raw):
    result={}
    for k in ('reference','action','specification','reasoning','answer'):
        matches=re.findall(r'<<'+k+r'>>\s*(.*?)\s*<</'+k+r'>>',raw,re.S)
        result[k]=matches[0] if len(matches)==1 else None
    result['valid_answer']=result['answer'] in ('YES','NO')
    result['valid_intent']=all(result[k] is not None for k in ('reference','action','specification','reasoning'))
    return result

def main():
    a=argparse.ArgumentParser();a.add_argument('--model',required=True);a.add_argument('--manifest',required=True);a.add_argument('--output',required=True);args=a.parse_args()
    import torch
    from PIL import Image
    from transformers import AutoProcessor,Qwen3VLForConditionalGeneration
    assert torch.cuda.device_count()==1,'Set exactly one CUDA_VISIBLE_DEVICES'
    torch.manual_seed(20261117);torch.cuda.set_per_process_memory_fraction(20*1024**3/torch.cuda.get_device_properties(0).total_memory,0)
    physical=os.environ.get('CUDA_VISIBLE_DEVICES','')
    assert physical.isdigit(),'Use a single numeric physical GPU index'
    def used():
        return int(subprocess.check_output(['nvidia-smi','-i',physical,'--query-gpu=memory.used','--format=csv,noheader,nounits'],text=True).strip())
    assert used()<100,'GPU occupied; do not load'
    started=time.monotonic();processor=AutoProcessor.from_pretrained(args.model,local_files_only=True)
    model=Qwen3VLForConditionalGeneration.from_pretrained(args.model,local_files_only=True,torch_dtype=torch.bfloat16,attn_implementation='sdpa').to('cuda:0').eval()
    def watch():
        while True:
            time.sleep(2)
            try:
                if used()-torch.cuda.memory_reserved()/1024**2>1024:
                    print('STOP: possible foreign GPU allocation',flush=True);os.kill(os.getpid(),signal.SIGINT);return
            except (ValueError,subprocess.SubprocessError):
                os.kill(os.getpid(),signal.SIGINT);return
    threading.Thread(target=watch,daemon=True).start()
    prompt=(Path(__file__).parents[1]/'configs/original_prompt.txt').read_text()
    seen=set();out=Path(args.output);out.parent.mkdir(parents=True,exist_ok=True)
    if out.exists():
        for line in out.read_text().splitlines():
            r=json.loads(line)
            if r.get('status')=='OK':seen.add((r['id'],r['condition']))
    for sample in json.loads(Path(args.manifest).read_text()):
        key=(sample['id'],sample['condition'])
        if key in seen:continue
        if time.monotonic()-started>21600:break
        row={'id':key[0],'condition':key[1],'intent_status':'UNVERIFIED','decision_gold':'UNVERIFIED'}
        try:
            images=[]
            for path in sample['images']:
                im=Image.open(path).convert('RGB');im.thumbnail((512,512));images.append(im)
            system=sample.get('system',prompt)
            text=sample['text']
            if sample['condition']=='gold':
                assert sample.get('review_status')=='HUMAN_VERIFIED','Unverified gold forbidden'
                text+='\nVerified editing operation: '+json.dumps({k:sample[k] for k in ('referent','action','specification')})
            elif sample['condition']=='draft-intent':
                text+='\nEditing operation (unverified annotation draft): '+json.dumps({k:sample[k] for k in ('referent','action','specification')})
            elif sample['condition']=='matched':text+='\n'+sample['neutral_context']
            messages=[{'role':'system','content':[{'type':'text','text':system}]},{'role':'user','content':[{'type':'image','image':im} for im in images]+[{'type':'text','text':text}]}]
            inputs=processor.apply_chat_template(messages,tokenize=True,add_generation_prompt=True,return_dict=True,return_tensors='pt').to('cuda:0')
            torch.cuda.reset_peak_memory_stats();torch.cuda.synchronize();t=time.monotonic()
            with torch.inference_mode():outputs=model.generate(**inputs,max_new_tokens=512,do_sample=False)
            torch.cuda.synchronize();tokens=outputs[0,inputs['input_ids'].shape[1]:];raw=processor.decode(tokens,skip_special_tokens=True)
            row.update(status='OK',input_tokens=int(inputs['input_ids'].shape[1]),raw=raw,parsed=parse(raw),seconds=time.monotonic()-t,output_tokens=len(tokens),hit_token_limit=len(tokens)==512,peak_allocated_gib=torch.cuda.max_memory_allocated()/1024**3,peak_reserved_gib=torch.cuda.max_memory_reserved()/1024**3,input_sha256=hashlib.sha256((system+text).encode()).hexdigest())
        except Exception as e:
            import traceback;traceback.print_exc()
            row.update(status='ERROR',error_type=type(e).__name__,error=str(e)[:400])
        with out.open('a') as f:f.write(json.dumps(row)+'\n');f.flush()
        print(json.dumps({k:v for k,v in row.items() if k not in ('raw','parsed','error')}),flush=True)
        if row.get('peak_reserved_gib',0)>20:break
if __name__=='__main__':main()
