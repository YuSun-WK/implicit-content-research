"""Build offline stage-1 HTML; supplied dossiers/images must be legally available."""
import argparse,json,hashlib
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--dossiers',required=True);p.add_argument('--output-dir',required=True);p.add_argument('--policy',required=True);a=p.parse_args();out=Path(a.output_dir);out.mkdir(parents=True,exist_ok=True)
raw=json.loads(Path(a.dossiers).read_text());assert len(raw)<=32
# No prediction data or prefilled model-derived risk annotation is accepted.
allowed={'group_id','source','instruction','images'}
for r in raw:
    if set(r)-allowed:raise ValueError('Unapproved dossier fields')
    for im in r['images']:
        path=(out/im['path']).resolve()
        if not path.is_relative_to(out.resolve()):raise ValueError('Unsafe asset path')
        if hashlib.sha256(path.read_bytes()).hexdigest()!=im['sha256']:raise ValueError('Image hash mismatch')
policy=Path(a.policy).read_text();data={'package_id':'KDIR-RN2-stage1-20261117','policy':policy,'policy_sha256':hashlib.sha256(policy.encode()).hexdigest(),'dossiers':raw}
template=(Path(__file__).parents[1]/'templates/review_template.html').read_text();html=template.replace('__DATA_JSON__',json.dumps(data,ensure_ascii=False).replace('</','<\\/'))
(out/'index.html').write_text(html);print('Built stage-1 dossiers:',len(raw),'No model outputs embedded.')
