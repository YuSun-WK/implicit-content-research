"""Export allowed telemetry from private runner logs. Never export raw model content."""
import argparse,json,hashlib,collections
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('private_jsonl');p.add_argument('output_json');a=p.parse_args();rows=[]
for line in Path(a.private_jsonl).read_text().splitlines():
    r=json.loads(line)
    fields=('id','condition','status','seconds','input_tokens','output_tokens','hit_token_limit','peak_allocated_gib','peak_reserved_gib','input_sha256','error_type')
    s={k:r[k] for k in fields if k in r}
    if r.get('status')=='OK':
        s.update(answer=r['parsed']['answer'],valid_answer=r['parsed']['valid_answer'],valid_intent_format=r['parsed']['valid_intent'],raw_output_sha256=hashlib.sha256(r['raw'].encode()).hexdigest(),intent_review='UNVERIFIED',safety_gold='UNVERIFIED')
    rows.append(s)
Path(a.output_json).write_text(json.dumps(rows,indent=2))
print(json.dumps({'completed_calls':sum(r['status']=='OK' for r in rows),'conditions':dict(collections.Counter(r['condition'] for r in rows if r['status']=='OK')),'gold_metrics':'Not computed without independent review'}))
