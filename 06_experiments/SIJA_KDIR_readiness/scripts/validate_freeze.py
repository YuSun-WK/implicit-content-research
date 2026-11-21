"""CPU-only freeze gate. Completeness checks cannot authenticate human activity."""
import json,argparse,hashlib
from pathlib import Path
from kdir_core import qualification_errors,canonical

def validate_groups(groups):
    if type(groups) is not list or len(groups)!=32:raise ValueError('Need 32 qualified groups')
    for g in groups:
        errors=qualification_errors(g)
        if errors:raise ValueError(str(g.get('group_id','?'))+': '+'; '.join(errors))
    if len({g['group_id'] for g in groups})!=32:raise ValueError('Duplicate group')
    if sum(g.get('split')=='dev' for g in groups)!=8 or sum(g.get('split')=='test' for g in groups)!=24:raise ValueError('Need 8 dev + 24 test')
    owners={}
    for g in groups:
        for k in ('source_pair_cluster','near_duplicate_cluster'):
            if not isinstance(g.get(k),str) or not g[k].strip():raise ValueError('Missing leakage cluster')
            previous=owners.setdefault((k,g[k]),g['split'])
            if previous!=g['split']:raise ValueError('Leakage across splits')
        if any(x in ('SIJA-329','SIJA-310') for x in g.get('source_ids',[])) and g['split']=='test':raise ValueError('Previously predicted sample in unseen test')
        for role in ('Iu','Is'):
            image=g.get('images',{}).get(role,{})
            path=Path(image.get('path',''))
            if not path.is_file():raise ValueError('Missing source image file')
            if hashlib.sha256(path.read_bytes()).hexdigest()!=image.get('sha256'):raise ValueError('Image hash mismatch')
    return {'status':'FROZEN','group_manifest_sha256':hashlib.sha256(canonical(groups)).hexdigest(),'group_ids':[g['group_id'] for g in groups],'model_inference_executed':False,'note':'Evidence record validation does not prove reviewers exist or labels are correct.'}

def main():
    p=argparse.ArgumentParser();p.add_argument('--groups',required=True);p.add_argument('--output',required=True);a=p.parse_args()
    result=validate_groups(json.loads(Path(a.groups).read_text()));Path(a.output).write_text(json.dumps(result,indent=2))
if __name__=='__main__':main()
