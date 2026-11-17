"""CPU only: refuse to freeze incomplete or overlapping groups."""
import json,argparse,hashlib
from pathlib import Path
from kdir_core import eligible,canonical
p=argparse.ArgumentParser();p.add_argument('--groups',required=True);p.add_argument('--output',required=True);a=p.parse_args();groups=json.loads(Path(a.groups).read_text())
assert len(groups)==32 and all(eligible(g) for g in groups),'Need 32 independently reviewed qualified groups'
assert len({g['group_id'] for g in groups})==32,'Duplicate group'
assert sum(g['split']=='dev' for g in groups)==8 and sum(g['split']=='test' for g in groups)==24
owners={}
for g in groups:
    for k in ('source_pair_cluster','near_duplicate_cluster'):
        assert g.get(k),'Missing leakage cluster'
        previous=owners.setdefault((k,g[k]),g['split']);assert previous==g['split'],'Leakage across splits'
    assert not any(x in ('SIJA-329','SIJA-310') for x in g.get('source_ids',[])) or g['split']!='test','Prior predicted sample cannot be unseen test'
    assert g.get('review_disagreements_resolved') is True
    assert all(g['four_cell_outcomes'].get(c) for c in ('Iu_er','Iu_en','Is_er','Is_en'))
    assert all(g['r_a_s'][o].get(k) for o in ('er','en') for k in ('referent','action','specification','instruction_evidence'))
    for role in ('Iu','Is'):
        path=Path(g['images'][role]['path']);assert path.is_file()
        assert hashlib.sha256(path.read_bytes()).hexdigest()==g['images'][role]['sha256']
Path(a.output).write_text(json.dumps({'status':'FROZEN','group_manifest_sha256':hashlib.sha256(canonical(groups)).hexdigest(),'group_ids':[g['group_id'] for g in groups],'model_inference_executed':False},indent=2))
