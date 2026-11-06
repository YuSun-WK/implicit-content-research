#!/usr/bin/env python3
"""Deterministic stratified sample and image integrity audit."""
import collections
import csv
import hashlib
import json
import pathlib
import random
import subprocess
import sys
from PIL import Image

ROOT=pathlib.Path(__file__).resolve().parents[1]
RUN=pathlib.Path(sys.argv[1])
DATA=ROOT/'data/manifests'
REV='3ac26e778db94a282711f463f22ba6db99643bee'
SEED=20261105

def writecsv(path,rows,fields):
    with path.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)

def fetch(path,target):
    target.parent.mkdir(parents=True,exist_ok=True)
    url=f'https://huggingface.co/datasets/Sandy124/TriggerBench/resolve/{REV}/{path}'
    tmp=target.with_suffix('.partial')
    subprocess.run(['curl','--http1.1','-fL','--retry','10','--retry-all-errors','--retry-delay','2','--max-time','180','-sS',url,'-o',str(tmp)],check=True)
    tmp.replace(target)

def main():
    RUN.mkdir(parents=True,exist_ok=False)
    pairs=list(csv.DictReader((DATA/'pair_manifest.csv').open(encoding='utf-8',newline='')))
    groups=collections.defaultdict(list)
    for p in pairs:
        if p['split']=='test' and p['valid']=='True':groups[p['category']].append(p)
    assert len(groups)==9 and all(len(v)>=4 for v in groups.values())
    rng=random.Random(SEED)
    order=[]; selected=[]
    for cat in sorted(groups):
        candidates=sorted(groups[cat],key=lambda p:int(p['index']))
        rng.shuffle(candidates)
        for rank,p in enumerate(candidates):order.append({'category':cat,'rank':rank,'pair_id':p['pair_id'],'selected':rank<4})
        selected.extend(candidates[:4])
    writecsv(RUN/'sampling_order.csv',order,list(order[0]))
    images=[]; failures=[]; hashes=collections.defaultdict(list)
    for p in selected:
        p.update(review_status='pending_review')
        for side in ('safe','unsafe'):
            hf=p[f'{side}_hf_path']
            local=RUN/'images'/hf
            rec={'pair_id':p['pair_id'],'side':side,'hf_path':hf,'local_path':str(local),'status':'ok'}
            try:
                if not local.exists():fetch(hf,local)
                b=local.read_bytes();rec['sha256']=hashlib.sha256(b).hexdigest()
                with Image.open(local) as im:
                    im.verify()
                with Image.open(local) as im:
                    rec.update(width=im.width,height=im.height,format=im.format)
                hashes[rec['sha256']].append((p['pair_id'],side))
                p[f'{side}_local_path']=str(local)
                p[f'{side}_sha256']=rec['sha256']
            except Exception as e:
                rec.update(status='failed',error=repr(e));failures.append(rec)
                p[f'{side}_local_path']='';p[f'{side}_sha256']=''
            images.append(rec)
    fields=list(selected[0])
    writecsv(RUN/'sample_manifest.csv',selected,fields)
    audit={'dataset_revision':REV,'seed':SEED,'selected_pairs':len(selected),'images':images,'failures':failures,
           'exact_duplicate_image_groups':[v for v in hashes.values() if len(v)>1],
           'review_status':'pending_review','replacement_policy':'no silent replacement; use sampling_order.csv rank 4 onward with explicit record'}
    (RUN/'image_audit.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2))
    print(json.dumps({'selected_pairs':len(selected),'downloaded_images':len(images)-len(failures),'failures':len(failures),'duplicate_groups':len(audit['exact_duplicate_image_groups'])}))
    if failures:sys.exit(2)

if __name__=='__main__':main()
