"""Run frozen two-pair protocols after pinned integrity gate; retain failures."""
import pathlib,subprocess,json,time,csv,shutil,datetime,sys
gpu_id=sys.argv[1] if len(sys.argv)>1 else '2'
R=pathlib.Path(__file__).resolve().parents[1];run=R/'runs/h1_resume_20261117_014439';smoke=run/'smoke';smoke.mkdir(exist_ok=True);py=str(R/'.venv/bin/python');model='Sandy124/ThinkingGuard-8B';rev='76892f9768ce828268265171f4bbc5dfb75eafc3';snap=R/'model_snapshots/Sandy124__ThinkingGuard-8B'/rev
end=datetime.datetime(2026,11,17,7,24,39,tzinfo=datetime.timezone.utc).timestamp()
def execute(label,args):
 with (run/(label+'.log')).open('w') as f:
  start=time.time();p=subprocess.run([py,*map(str,args)],cwd=R,stdout=f,stderr=subprocess.STDOUT,timeout=max(1,end-time.time()))
 with (run/'phases.jsonl').open('a') as f:f.write(json.dumps(dict(phase=label,start=start,end=time.time(),exit=p.returncode))+'\n')
 return p.returncode
if execute('model_integrity_gate',['scripts/audit_model_cache.py',model,snap]):raise RuntimeError('model integrity gate failed')
shutil.copyfile(R/'runs/h1_k0_recovery_20261107_034443/sample_manifest.csv',smoke/'sample_manifest.csv')
status={}
for protocol in ['unified','official_five_step']:
 gpu=subprocess.check_output(['nvidia-smi','-i',gpu_id,'--query-gpu=memory.used,utilization.gpu','--format=csv,noheader,nounits'],text=True).strip().split(',')
 if int(gpu[0])>=100 or int(gpu[1])!=0:raise RuntimeError(f'GPU {gpu_id} busy')
 code=execute('smoke_'+protocol,['scripts/run_inference.py',smoke,model,'--protocol',protocol,'--limit-pairs',2,'--gpu',gpu_id,'--image-root',R/'image_cache_h1_k0_recovery','--model-path',snap]);status[protocol]={'inference_exit':code}
 records=[json.loads(l) for l in (smoke/'predictions.jsonl').read_text().splitlines() if json.loads(l)['protocol']==protocol] if (smoke/'predictions.jsonl').exists() else []
 status[protocol].update(records=len(records),valid=sum(p['parse_status']=='ok' for p in records),peak_gib=max([p['peak_gpu_gib'] for p in records],default=None))
 if records:status[protocol]['evaluation_exit']=execute('smoke_evaluation_'+protocol,['scripts/evaluate.py',smoke,'--model-id',model,'--model-revision',rev,'--protocol',protocol,'--limit-pairs',2])
 (run/'smoke_status.json').write_text(json.dumps(status,indent=2))
 # Failures leave logs/raw outputs; an official-protocol smoke may still diagnose format issues.
 if not records:break
print(json.dumps(status),flush=True)
