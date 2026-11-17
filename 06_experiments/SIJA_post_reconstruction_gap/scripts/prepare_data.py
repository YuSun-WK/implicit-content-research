"""Metadata seed selection and ZIP Range extraction; private destinations only."""
import argparse,json,random,struct,zlib,urllib.request,hashlib,time
from pathlib import Path
REV='4087764c55ea76946bac6634aa4d63b2ad7bb5a0'
def select(rows,n=4):
    rows=sorted([x for x in rows if x['category']==['I7']],key=lambda x:x['id'])
    random.Random(20261117).shuffle(rows);return rows[:n]
def read_range(a,b):
    url=f'https://huggingface.co/datasets/xianminye/SI2ESBench/resolve/{REV}/SI2ESBench.zip?start={a}'
    for attempt in range(3):
        try:
            r=urllib.request.urlopen(urllib.request.Request(url,headers={'Range':f'bytes={a}-{b}'}),timeout=20)
            if r.status!=206:raise ValueError('Range unsupported')
            data=r.read(b-a+2)
            if len(data)!=b-a+1:raise ValueError('Wrong range length')
            return data
        except Exception:
            if attempt==2:raise
            time.sleep(1)
def extract(entry):
    offset=entry['offset'];h=struct.unpack('<4s5H3L2H',read_range(offset,offset+29));start=offset+30+h[-2]+h[-1]
    payload=read_range(start,start+entry['compressed']-1)
    raw=zlib.decompress(payload,-15) if h[3]==8 else payload
    if len(raw)!=entry['size'] or zlib.crc32(raw)!=entry['crc']:raise ValueError('CRC/size mismatch')
    return raw
if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--metadata',required=True);a.add_argument('--entries',required=True);a.add_argument('--private-dir',required=True);args=a.parse_args()
    from PIL import Image
    import io
    dest=Path(args.private_dir);dest.mkdir(exist_ok=True,parents=True);entries={e['name']:e for e in json.loads(Path(args.entries).read_text())};selected=select(json.loads(Path(args.metadata).read_text()));manifest=[];audit=[]
    for row in selected:
        paths=[]
        for name in (row['image-path'],f"cue_images/{row['id']}.png"):
            rec={'id':row['id'],'kind':'source' if name==row['image-path'] else 'cue'}
            try:
                path=dest/name;path.parent.mkdir(parents=True,exist_ok=True)
                raw=path.read_bytes() if path.exists() else extract(entries[name]);im=Image.open(io.BytesIO(raw));im.load();path.write_bytes(raw);paths.append(str(path));rec.update(status='DECODED',size=list(im.size),sha256=hashlib.sha256(raw).hexdigest())
            except Exception as e:rec.update(status='ERROR',error_type=type(e).__name__)
            audit.append(rec)
        if len(paths)==2:manifest.append(dict(id='SIJA-'+str(row['id']),condition='natural',images=paths,text=row['prompt']))
    (dest/'manifest.json').write_text(json.dumps(manifest));(dest/'decode_audit.json').write_text(json.dumps(audit,indent=2));print(json.dumps(audit),flush=True)
