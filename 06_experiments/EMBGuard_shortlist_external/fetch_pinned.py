"""Resume the three fixed EMBGuard Parquet files and verify full SHA-256."""
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
from pathlib import Path
import random
import requests
import sys
import time

REV='c89d9e597149e22f34fc7c09e5e02125c2e1a521'
FILES={
 'causal_risky':(264506097,'7351b8ddfda9bb7c09ca7a4a46d85e4d3502da225780748304e59bbb870ed982'),
 'decoupled_benign':(264506288,'10dfb255bf21e7f753a239603919e02b988fa6c50256e14b723a0828a9ef3ee1'),
 'selective_risky':(401919122,'e1c533fc53a9153ab240e747644eb4f0a227abdcf17ff59187dbc9b2cb1338e4'),
}
PART=4*1024*1024


def fetch_one(root,name,size,expected):
    url=f'https://huggingface.co/datasets/EMBGuard/EMBGuardTest_v3/resolve/{REV}/data/{name}-00000-of-00001.parquet'
    pieces=root/(name+'.parts');pieces.mkdir(parents=True,exist_ok=True)
    bounds=[(i,min(i+PART,size)-1) for i in range(0,size,PART)]
    def signed():
        for n in range(15):
            try:
                r=requests.head(url,params={'download':'true','attempt':n},allow_redirects=False,timeout=(8,20))
                if r.status_code==302 and r.headers.get('x-linked-etag','').strip('"')==expected:return r.headers['location']
            except requests.RequestException:pass
            time.sleep(1)
        raise RuntimeError('No signed URL for '+name)
    def fetch(a,b,link):
        p=pieces/f'{a:012d}.part'
        if p.exists() and p.stat().st_size==b-a+1:return
        for n in range(8):
            try:
                r=requests.get(link,headers={'Range':f'bytes={a}-{b}','Accept-Encoding':'identity'},timeout=(8,25))
                if r.status_code==206 and r.headers.get('Content-Range')==f'bytes {a}-{b}/{size}' and len(r.content)==b-a+1:
                    p.write_bytes(r.content);return
            except requests.RequestException:pass
            time.sleep(random.uniform(.1,.7))
        raise RuntimeError(f'{name} failed range {a}-{b}')
    pending=[(a,b) for a,b in bounds if not (pieces/f'{a:012d}.part').exists() or (pieces/f'{a:012d}.part').stat().st_size!=b-a+1]
    print(name,'present',len(bounds)-len(pending),'/',len(bounds),flush=True)
    while pending:
        link=signed();batch=pending[:30];errors=[]
        with ThreadPoolExecutor(max_workers=12) as pool:
            for f in as_completed([pool.submit(fetch,a,b,link) for a,b in batch]):
                try:f.result()
                except RuntimeError as e:errors.append(str(e))
        pending=[(a,b) for a,b in bounds if not (pieces/f'{a:012d}.part').exists() or (pieces/f'{a:012d}.part').stat().st_size!=b-a+1]
        print(name,'complete',len(bounds)-len(pending),'/',len(bounds),'errors',len(errors),flush=True)
        if len(errors)==len(batch):raise RuntimeError('No progress; rerun later')
    target=root/f'{name}.parquet';h=hashlib.sha256()
    with target.open('wb') as out:
        for a,b in bounds:
            raw=(pieces/f'{a:012d}.part').read_bytes();out.write(raw);h.update(raw)
    if h.hexdigest()!=expected:target.unlink();raise RuntimeError(name+' SHA-256 mismatch')
    print(name,'verified',size,expected,flush=True)


def main():
    root=Path(sys.argv[1]);root.mkdir(parents=True,exist_ok=True)
    for name,(size,digest) in FILES.items():fetch_one(root,name,size,digest)


if __name__=='__main__':main()
