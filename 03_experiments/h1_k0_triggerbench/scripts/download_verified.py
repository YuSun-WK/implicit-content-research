"""Bounded Range transfer: durable independently hashed blocks, official final SHA256."""
import argparse,concurrent.futures,hashlib,json,os,pathlib,shutil,time,requests
from audit_model_cache import REVISIONS,SHARDS,sha256_file
p=argparse.ArgumentParser();p.add_argument('--model',default='Sandy124/ThinkingGuard-8B');p.add_argument('--host',default='https://huggingface.co');p.add_argument('--run-dir',type=pathlib.Path,default=pathlib.Path('runs/h1_autonomous_20261116_064613'));p.add_argument('--block-mib',type=int,default=16);p.add_argument('--deadline',type=float,required=True);a=p.parse_args()
rev=REVISIONS[a.model];root=pathlib.Path('model_snapshots')/a.model.replace('/','__')/rev;root.mkdir(parents=True,exist_ok=True)
a.run_dir.mkdir(parents=True,exist_ok=True)
log=a.run_dir/'download.jsonl'
def emit(**kw):
 with log.open('a') as f:f.write(json.dumps(dict(time=time.time(),host=a.host,block_mib=a.block_mib,**kw))+'\n')
meta=requests.get(f'https://huggingface.co/api/models/{a.model}/revision/{rev}?blobs=true',timeout=30);meta.raise_for_status();meta=meta.json();assert meta['sha']==rev
(root/'official_metadata.json').write_text(json.dumps(meta,indent=2))
for name,(size,digest) in SHARDS[a.model].items():
 item=next(s for s in meta['siblings'] if s['rfilename']==name);assert item['lfs']['sha256']==digest and item['size']==size
cache=pathlib.Path.home()/'.cache/huggingface/hub'/('models--'+a.model.replace('/','--'))/'snapshots'/rev
for item in meta['siblings']:
 name=item['rfilename']
 if name in SHARDS[a.model] or name.startswith('.') or '/' in name:continue
 dest=root/name
 source=cache/name
 if source.is_file():shutil.copyfile(source,dest)
 elif not dest.exists():
  r=requests.get(f'{a.host}/{a.model}/resolve/{rev}/{name}',timeout=(15,60));r.raise_for_status();dest.write_bytes(r.content)
 # Verify git blob for non-LFS files and SHA256 for LFS small files.
 data=dest.read_bytes();expected=item.get('lfs',{}).get('sha256')
 if expected:assert hashlib.sha256(data).hexdigest()==expected
 else:assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==item['blobId']
block=a.block_mib*1024*1024
for name,(size,digest) in SHARDS[a.model].items():
 dest=root/name
 if dest.exists() and dest.stat().st_size==size and sha256_file(dest)==digest:emit(event='reuse',file=name);continue
 parts=root/(name+f'.blocks{a.block_mib}');parts.mkdir(exist_ok=True)
 def fetch(i):
  lo=i*block;hi=min(size,lo+block)-1;target=parts/str(i);receipt=parts/(str(i)+'.json')
  if target.exists() and receipt.exists() and target.stat().st_size==hi-lo+1 and sha256_file(target)==json.loads(receipt.read_text())['sha256']:return
  for attempt in range(3):
   if time.time()>a.deadline:raise TimeoutError('global deadline')
   started=time.monotonic()
   try:
    # Unique query prevents intermediary caches from reusing another byte range.
    url=f'{a.host}/{a.model}/resolve/{rev}/{name}?download=true&block={i}&nonce={time.time_ns()}'
    with requests.get(url,headers={'Range':f'bytes={lo}-{hi}'},stream=True,timeout=(15,45)) as r:
     assert r.status_code==206,(r.status_code,'Range unsupported')
     assert r.headers.get('Content-Range')==f'bytes {lo}-{hi}/{size}',r.headers.get('Content-Range')
     tmp=parts/(str(i)+'.tmp');n=0;h=hashlib.sha256()
     with tmp.open('wb') as f:
      for c in r.iter_content(1024*1024):
       if time.time()>a.deadline:raise TimeoutError('global deadline')
       n+=len(c);assert n<=hi-lo+1;f.write(c);h.update(c)
      f.flush();os.fsync(f.fileno())
     assert n==hi-lo+1
     tmp.replace(target);receipt.write_text(json.dumps(dict(bytes=n,sha256=h.hexdigest())))
     emit(event='block',file=name,block=i,bytes=n,seconds=time.monotonic()-started,attempt=attempt);return
   except Exception as e:emit(event='error',file=name,block=i,attempt=attempt,error=type(e).__name__+': '+str(e)[:180])
  raise RuntimeError(f'block {i} failed after 3 attempts')
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
  for _ in pool.map(fetch,range((size+block-1)//block)):pass
 tmp=root/(name+'.assembling')
 with tmp.open('wb') as out:
  for i in range((size+block-1)//block):
   with (parts/str(i)).open('rb') as f:shutil.copyfileobj(f,out)
  out.flush();os.fsync(out.fileno())
 assert tmp.stat().st_size==size and sha256_file(tmp)==digest
 tmp.replace(dest);emit(event='verified',file=name,bytes=size,sha256=digest)
print(root,flush=True)
