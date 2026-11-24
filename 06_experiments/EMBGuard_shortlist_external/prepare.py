"""Verify published EMBGuard panels, decode image identities, create private scoring rows."""
from collections import Counter, defaultdict
import csv
import hashlib
import io
import json
from pathlib import Path
import sys

from PIL import Image
import pyarrow.parquet as pq

HERE=Path(__file__).resolve().parent
FILES={'causal_risky':'7351b8ddfda9bb7c09ca7a4a46d85e4d3502da225780748304e59bbb870ed982',
       'decoupled_benign':'10dfb255bf21e7f753a239603919e02b988fa6c50256e14b723a0828a9ef3ee1',
       'selective_risky':'e1c533fc53a9153ab240e747644eb4f0a227abdcf17ff59187dbc9b2cb1338e4'}


def sha(x):return hashlib.sha256(x).hexdigest()


def write(path,records,fields):
    with path.open('w',newline='') as f:
        w=csv.DictWriter(f,fields);w.writeheader();w.writerows(records)


def main():
    private=Path(sys.argv[1]);(private/'images').mkdir(parents=True,exist_ok=True)
    rows={};decoded={}
    for name,digest in FILES.items():
        path=private/(name+'.parquet')
        with path.open('rb') as f:assert hashlib.file_digest(f,'sha256').hexdigest()==digest
        table=pq.read_table(path,columns=['id','image','image_path','situation','action','risk','pair_item_id'])
        records=table.to_pylist()
        rows[name]=[]
        for r in records:
            raw=(r.pop('image') or {}).get('bytes')
            r['image_error']=''
            if not raw:r['image_error']='missing_bytes';rows[name].append(r);continue
            bsha=sha(raw)
            if bsha not in decoded:
                try:
                    with Image.open(io.BytesIO(raw)) as im:
                        rgb=im.convert('RGB')
                        pix=sha(f'{rgb.width}x{rgb.height}:RGB:'.encode()+rgb.tobytes())
                    (private/'images'/bsha).write_bytes(raw)
                    decoded[bsha]=(pix,'')
                except (OSError,ValueError):decoded[bsha]=('', 'decode_failed')
            r['image_sha256']=bsha
            r['pixel_sha256'],r['image_error']=decoded[bsha]
            rows[name].append(r)
    exclusions=[];groups=[]
    def reject(panel,key,reason):exclusions.append({'panel':panel,'group':key,'reason':reason})
    a=defaultdict(list);b=defaultdict(list)
    for r in rows['causal_risky']:a[(r['image_path'],r['situation'])].append(r)
    for r in rows['decoupled_benign']:b[(r['image_path'],r['situation'])].append(r)
    for key in sorted(set(a)|set(b)):
        gid=sha(json.dumps(['mixed',*key],ensure_ascii=False).encode())[:24]
        left,right=a.get(key,[]),b.get(key,[])
        if len(left)!=1 or len(right)!=1:reject('mixed',gid,'not_one_to_one');continue
        x,y=left[0],right[0]
        if x['image_error'] or y['image_error']:reject('mixed',gid,'image_unavailable');continue
        if x['pixel_sha256']!=y['pixel_sha256']:reject('mixed',gid,'different_decoded_image');continue
        if (x['risk'],y['risk'])!=('O','X'):reject('mixed',gid,'wrong_label_pair');continue
        if x['action']==y['action']:reject('mixed',gid,'identical_actions');continue
        groups.append(('mixed',gid,x,y))
    sel=rows['selective_risky'];by_id={r['id']:r for r in sel}
    assert len(by_id)==len(sel)
    seen=set()
    for r in sel:
        if r['id'] in seen:continue
        other=by_id.get(r['pair_item_id'])
        gid=sha(json.dumps(['all_reject',*sorted([r['id'],r['pair_item_id']])]).encode())[:24]
        if other is None or other['pair_item_id']!=r['id'] or other['id']==r['id']:
            reject('all_reject',gid,'not_reciprocal');seen.add(r['id']);continue
        seen.update([r['id'],other['id']])
        if r['image_error'] or other['image_error']:reject('all_reject',gid,'image_unavailable');continue
        if (r['image_path'],r['situation'])!=(other['image_path'],other['situation']):reject('all_reject',gid,'different_scene');continue
        if r['pixel_sha256']!=other['pixel_sha256']:reject('all_reject',gid,'different_decoded_image');continue
        if r['risk']!='O' or other['risk']!='O':reject('all_reject',gid,'wrong_label_pair');continue
        if r['action']==other['action']:reject('all_reject',gid,'identical_actions');continue
        groups.append(('all_reject',gid,r,other))
    scoring=[];manifest=[];pairs=[]
    for panel,gid,x,y in groups:
        ids=[]
        for r in (x,y):
            rid=sha(('EMBGuardTest_v3:'+r['id']).encode())[:24]
            row={'id':rid,'image_sha256':r['image_sha256'],'pixel_sha256':r['pixel_sha256'],
                 'image_identity':r['pixel_sha256'],'scene':gid,'partition':'external','panel':panel,
                 'risk':r['risk'],'tie_key':sha(r['id'].encode()),'action':r['action']}
            scoring.append(row)
            manifest.append({k:row[k] for k in ('id','scene','panel','risk','image_sha256','pixel_sha256','image_identity','tie_key')})
            ids.append(rid)
        pairs.append({'scene':gid,'panel':panel,'image_identity':x['pixel_sha256'],'first_id':ids[0],'second_id':ids[1]})
    assert len({r['id'] for r in scoring})==len(scoring)
    write(HERE/'splits.csv',manifest,list(manifest[0]))
    write(HERE/'groups.csv',pairs,list(pairs[0]))
    write(HERE/'excluded_groups.csv',exclusions,['panel','group','reason'])
    (private/'rows.json').write_text(json.dumps(scoring,ensure_ascii=False))
    summary={'published_rows':{name:len(v) for name,v in rows.items()},
             'usable_groups':dict(Counter(g[0] for g in groups)),
             'usable_rows':len(scoring),'unique_pixels':len({r['pixel_sha256'] for r in scoring}),
             'panel_images':{panel:len({g[2]['pixel_sha256'] for g in groups if g[0]==panel}) for panel in ('mixed','all_reject')},
             'overlap_panel_images':len({g[2]['pixel_sha256'] for g in groups if g[0]=='mixed'} & {g[2]['pixel_sha256'] for g in groups if g[0]=='all_reject'}),
             'excluded_groups':len(exclusions),'excluded_reasons':dict(Counter(e['reason'] for e in exclusions)),
             'dataset_revision':'c89d9e597149e22f34fc7c09e5e02125c2e1a521','parquet_sha256':FILES}
    (HERE/'data_audit.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))


if __name__=='__main__':main()
