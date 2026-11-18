"""CPU-only preparation. Reuse verified original bytes; never imports inference code."""
import argparse,csv,datetime,hashlib,hmac,io,json,os,pathlib,random,secrets,shutil,subprocess,urllib.request,zipfile
from PIL import Image
BASE='0a043abbf575d6b21f8d4095dbdfba7bad880465';AUDIT='e6d80b030d43918ca502091717e9334aaab5b561';REV='3ac26e778db94a282711f463f22ba6db99643bee'
MANIFEST='03_experiments/h1_k0_triggerbench/runs/h1_k1_20261117_060147/formal_unified/sample_manifest.csv';PRED=MANIFEST.replace('sample_manifest.csv','predictions.jsonl');K2='03_experiments/h1_k2_research_audit/H1_K2_Counterfactual_36.csv'
ROOT=pathlib.Path(__file__).resolve().parents[1];REPO=ROOT.parents[1]
def sha(data):return hashlib.sha256(data).hexdigest()
def gitbytes(commit,path):return subprocess.check_output(['git','show',f'{commit}:{path}'],cwd=REPO)
def stable_write(path,data):
 path=pathlib.Path(path);path.parent.mkdir(parents=True,exist_ok=True)
 if isinstance(data,str):data=data.encode()
 if path.exists():
  if path.read_bytes()!=data:raise RuntimeError(f'Existing file differs; refusing overwrite: {path}')
 else:path.write_bytes(data)
def jbytes(x):return (json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode()
def anonymous_layout(rows,seed):
 def ident(domain,value,n=20):return hmac.new(seed,(domain+'\0'+value).encode(),hashlib.sha256).hexdigest()[:n]
 def rng(domain):return random.Random(int(ident('shuffle',domain,64),16))
 result={}
 for reviewer in ['ReviewerA','ReviewerB']:
  singles=[];pairs=[]
  for row in rows:
   pid=row['pair_id']
   for side in ['safe','unsafe']:
    key=pid+'\0'+side;singles.append({'id':'S-'+ident(reviewer+'-single',key,12),'pair_id':pid,'side':side,'image':'assets/'+ident(reviewer+'-image',key)+'.png'})
  rng(reviewer+'-single-order').shuffle(singles);prng=rng(reviewer+'-pairs');ordered=list(rows);prng.shuffle(ordered)
  lookup={(s['pair_id'],s['side']):s for s in singles}
  for row in ordered:
   pid=row['pair_id'];left='safe' if prng.getrandbits(1) else 'unsafe';right='unsafe' if left=='safe' else 'safe';pairs.append({'id':'P-'+ident(reviewer+'-pair',pid,12),'pair_id':pid,'left_side':left,'right_side':right,'left':lookup[pid,left]['image'],'right':lookup[pid,right]['image']})
  result[reviewer]={'package_id':'K3-'+ident('package',reviewer),'singles':singles,'pairs':pairs}
 return result

def locate(row,side,oldroot,private):
 rel=pathlib.PurePosixPath(row[side+'_hf_path'])
 if rel.is_absolute() or '..' in rel.parts:raise ValueError('invalid dataset path')
 expected=row[side+'_sha256'];candidates=[oldroot/'image_cache_h1_k0_recovery'/str(rel),oldroot/row[side+'_local_path'],oldroot/'runs/h1_k0_recovery_20261107_034443/images'/str(rel),pathlib.Path.home()/'.cache/huggingface/hub/datasets--Sandy124--TriggerBench/snapshots'/REV/str(rel)]
 failures=[]
 def inspect(path,origin):
  data=path.read_bytes()
  if sha(data)!=expected:raise ValueError('SHA256 mismatch')
  with Image.open(io.BytesIO(data)) as im:im.verify()
  with Image.open(io.BytesIO(data)) as im:im.load();size=list(im.size);mode=im.mode;fmt=im.format;info=im.info
  if fmt!='PNG':raise ValueError('unexpected original format')
  # Do not strip/rewrite metadata. Fail if metadata itself carries source-label paths.
  metadata=json.dumps(info,default=str).lower()
  if any(t in metadata for t in ['_safe.png','_unsafe.png','test/images_test/','huggingface.co/','pair_id']):raise ValueError('source identity in image metadata')
  return data,dict(source=str(path),origin=origin,sha256=expected,bytes=len(data),size=size,mode=mode,format=fmt,decode=True,metadata_identity_leak=False,failures=failures)
 for p in candidates:
  if p.is_file():
   try:return inspect(p,'verified_existing_file')
   except Exception as e:failures.append(dict(source=str(p),error=type(e).__name__,reason=str(e)))
 url=f'https://huggingface.co/datasets/Sandy124/TriggerBench/resolve/{REV}/{rel}'
 for attempt in range(2):
  try:
   with urllib.request.urlopen(url,timeout=30) as response:data=response.read()
   if sha(data)!=expected:raise ValueError('download SHA256 mismatch')
   path=private/'acquired'/f'{expected}.png';stable_write(path,data);return inspect(path,'fixed_revision_download')
  except Exception as e:failures.append(dict(source=url,attempt=attempt,error=type(e).__name__))
 raise RuntimeError('Image unavailable after bounded attempts; retained failures: '+json.dumps(failures))

def build(oldroot):
 private=ROOT/'private';private.mkdir(exist_ok=True);os.chmod(private,0o700)
 seedpath=private/'seeds.json'
 if not seedpath.exists():stable_write(seedpath,jbytes({'algorithm':'HMAC-SHA256 domains + Python Random MT19937','root_seed':secrets.token_hex(32)}));os.chmod(seedpath,0o600)
 seed=bytes.fromhex(json.loads(seedpath.read_text())['root_seed']);raw=gitbytes(BASE,MANIFEST);predraw=gitbytes(BASE,PRED);k2raw=gitbytes(AUDIT,K2)
 rows=list(csv.DictReader(io.StringIO(raw.decode(),newline='')));screen=list(csv.DictReader(io.StringIO(k2raw.decode(),newline='')));preds=[json.loads(l) for l in predraw.decode().splitlines()];assert len(rows)==36 and len({r['pair_id'] for r in rows})==36 and len(preds)==180
 cross={x['pair_id']:x for x in screen};assert len(cross)==36
 for row in rows:
  a=cross[row['pair_id']];assert row['text']==a['text']
  for side in ['safe','unsafe']:assert row[side+'_sha256']==a[side+'_sha256']
 layouts=anonymous_layout(rows,seed);byid={r['pair_id']:r for r in rows};index={(p['pair_id'],p['input_condition'],p['side']):p for p in preds};assert len(index)==180
 baseline=[]
 for row in rows:
  pid=row['pair_id'];baseline.append({'pair_id':pid,'category':row['category'],'text':row['text'],'labels':{'safe':'Safe','unsafe':'Unsafe'},'joint':{s:index[pid,'joint',s]['parsed_prediction'] for s in ['safe','unsafe']},'image_only':{s:index[pid,'image_only',s]['parsed_prediction'] for s in ['safe','unsafe']},'text_only':index[pid,'text_only','pair']['parsed_prediction'],'candidate_11':index[pid,'joint','unsafe']['parsed_prediction']=='Safe' and index[pid,'image_only','unsafe']['parsed_prediction']=='Unsafe'})
 assert sum(x['candidate_11'] for x in baseline)==11
 registry={'schema_version':'H1K3-review-1.0','source_commit':BASE,'audit_commit':AUDIT,'dataset_revision':REV,'source_hashes':{MANIFEST:sha(raw),PRED:sha(predraw),K2:sha(k2raw)},'reviewers':layouts,'baseline':baseline}
 stable_write(private/'registry.json',jbytes(registry));os.chmod(private/'registry.json',0o600)
 stable_write(private/'original_manifest.csv',raw);stable_write(private/'original_predictions.jsonl',predraw)
 images={};integrity=[]
 for row in rows:
  for side in ['safe','unsafe']:
   data,record=locate(row,side,oldroot,private);images[row['pair_id'],side]=data;integrity.append(dict(pair_id=row['pair_id'],side=side,hf_path=row[side+'_hf_path'],expected_sha256=row[side+'_sha256'],**record))
 schema=json.loads((ROOT/'schema.json').read_text());guide=(ROOT/'H1_K3_Review_Guidelines.md').read_bytes()
 for reviewer,layout in layouts.items():
  package=ROOT/'packages'/reviewer;package.mkdir(parents=True,exist_ok=True)
  public={'schema_version':schema['schema_version'],'reviewer_id':reviewer,'package_id':layout['package_id'],'singles':[{'id':s['id'],'text':byid[s['pair_id']]['text'],'image':s['image']} for s in layout['singles']],'pairs':[{'id':p['id'],'text':byid[p['pair_id']]['text'],'left':p['left'],'right':p['right']} for p in layout['pairs']]}
  for name in ['index.html','app.js','style.css']:stable_write(package/name,(ROOT/'templates'/name).read_bytes())
  stable_write(package/'materials.js','window.REVIEW_SCHEMA='+json.dumps(schema,ensure_ascii=True)+';\nwindow.REVIEW_DATA='+json.dumps(public,ensure_ascii=True)+';\n');stable_write(package/'GUIDE.md',guide)
  for s in layout['singles']:stable_write(package/s['image'],images[s['pair_id'],s['side']])
  for stage,items in [(1,layout['singles']),(2,layout['pairs'])]:
   idfield='anonymous_sample_id' if stage==1 else 'anonymous_pair_id';columns=['schema_version','package_id','reviewer_id','stage','export_kind','reviewer_attestation','exported_at','phase1_locked_at','test_marker',idfield,*schema['stage'+str(stage)],'submitted_at'];buf=io.StringIO(newline='');w=csv.DictWriter(buf,fieldnames=columns);w.writeheader()
   for item in items:w.writerow({'schema_version':schema['schema_version'],'package_id':layout['package_id'],'reviewer_id':reviewer,'stage':stage,'export_kind':'draft',idfield:item['id']})
   stable_write(package/f'review_form_stage{stage}.csv',buf.getvalue())
 stable_write(private/'image_integrity.json',jbytes(integrity))
 # Source filesystem byte hashes, not file access timestamps. No old path is written.
 oldfiles={str(oldroot/'runs/h1_k1_20261117_060147/formal_unified'/name):sha((oldroot/'runs/h1_k1_20261117_060147/formal_unified'/name).read_bytes()) for name in ['sample_manifest.csv','predictions.jsonl','model_revisions.json']};stable_write(private/'old_files_hashes.json',jbytes(oldfiles))
 stable_write(private/'RECOVERY.md','仅协调人保存。本目录含匿名映射、种子、原标签及模型输出，不发送审核者，不放入HTTP根或公开仓库。seeds.json与registry.json须一起备份；固定源码和原Manifest可重建相同匿名ID/顺序。已存在文件不一致时生成器拒绝覆盖。真实人审导出另放results或private/received，保持版本，不覆盖。\n')
 files={str(p.relative_to(ROOT/'packages')):sha(p.read_bytes()) for p in (ROOT/'packages').rglob('*') if p.is_file()};stable_write(private/'package_files.json',jbytes(files))
 artifacts=ROOT/'artifacts';artifacts.mkdir(exist_ok=True)
 def make_zip(path,members):
  if path.exists():
   with zipfile.ZipFile(path) as z:assert {n:sha(z.read(n)) for n in z.namelist()}=={n:sha(p.read_bytes()) for p,n in members}
   return
  with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED) as z:
   for p,name in members:z.write(p,name)
 for reviewer in layouts:make_zip(artifacts/f'H1_K3_{reviewer}.zip',[(p,str(p.relative_to(ROOT/'packages'/reviewer))) for p in sorted((ROOT/'packages'/reviewer).rglob('*')) if p.is_file()])
 make_zip(artifacts/'H1_K3_Review_Materials.zip',[(p,str(p.relative_to(ROOT/'packages'))) for p in sorted((ROOT/'packages').rglob('*')) if p.is_file()])
 print(json.dumps({'state':'PREPARED_FOR_HUMAN_REVIEW','human_state':'HUMAN_REVIEW_PENDING','verified_images':len(integrity),'reused':sum(x['origin']=='verified_existing_file' for x in integrity),'downloaded':sum(x['origin']=='fixed_revision_download' for x in integrity),'reviewers':2,'sides_per_reviewer':72,'pairs_per_reviewer':36}))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--old-root',type=pathlib.Path,default=pathlib.Path('/home/ubuntu/data/project/h1-cf-killtest'));a=p.parse_args();build(a.old_root)
