"""Stage 2 is a separate artifact, created only after a frozen reviewed manifest."""
import argparse,json,html
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--freeze',required=True);p.add_argument('--predictions',required=True);p.add_argument('--output',required=True);a=p.parse_args();freeze=json.loads(Path(a.freeze).read_text());assert freeze.get('status')=='FROZEN'
rows=[json.loads(l) for l in Path(a.predictions).read_text().splitlines()]
assert all(r.get('group_id') in freeze['group_ids'] for r in rows)
body='<h1>第二阶段：冻结输入审核后的预测核验</h1><p>不回写阶段一；归因与分歧单独保存。</p>'
for r in rows:body+='<article><h2>'+html.escape(r['group_id'])+'</h2><pre>'+html.escape(json.dumps(r,ensure_ascii=False,indent=2))+'</pre></article>'
Path(a.output).write_text('<!doctype html><meta charset="utf-8">'+body)
