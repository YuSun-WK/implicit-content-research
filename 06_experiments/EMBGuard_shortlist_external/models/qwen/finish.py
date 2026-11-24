"""Merge the pilot and worker scores and verify one score record per released candidate."""
import argparse
import csv
import json
import math
from pathlib import Path


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('directory',type=Path)
    args=ap.parse_args()
    root=args.directory
    settings=json.loads((root/'settings.json').read_text())
    with (root/'splits.csv').open(newline='') as f:
        expected={r['id']:r for r in csv.DictReader(f)}
    scores={}
    paths=[root/'pilot_scores.jsonl',*sorted(root.glob('scores_[0-9][0-9].jsonl'))]
    for path in paths:
        for line in path.read_text().splitlines():
            r=json.loads(line)
            key=r['id']
            assert key in expected and key not in scores
            if r['status']=='ok':
                assert r['answer_token_ids']==settings['answer_token_ids']
                assert r['revision']==settings['model_revision']
                assert r['model']==settings['model']
                assert r['scene']==expected[key]['scene']
                assert math.isfinite(r['risk_score']) and r['risk_score']==r['logp_unsafe']-r['logp_safe']
            scores[key]=r
    missing=set(expected)-set(scores)
    for key in missing:
        scores[key]={'id':key,'status':'error','error_type':'missing_score'}
    ordered=[scores[key] for key in expected]
    with (root/'scores.jsonl').open('x') as f:
        for row in ordered:
            f.write(json.dumps(row)+'\n')
    with (root/'failures.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=['id','partition','scene','reason'])
        w.writeheader()
        for r in ordered:
            if r['status']!='ok':
                info=expected[r['id']]
                w.writerow({'id':r['id'],'partition':info['partition'],'scene':info['scene'],
                            'reason':r.get('error_type',r['status'])})
    print(len(scores),'candidate records;',sum(r['status']!='ok' for r in ordered),'failures')


if __name__=='__main__':
    main()
