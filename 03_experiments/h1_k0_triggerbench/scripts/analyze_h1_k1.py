"""Frozen-manifest error audit: retain every pair, flag confounds without relabelling."""
import pathlib,json,csv,random,hashlib,re,statistics,collections
try:
 from scripts.evaluate import wilson
except ModuleNotFoundError:
 from evaluate import wilson

def analyze(root):
 root=pathlib.Path(root);run=root/'formal_unified';manifest=list(csv.DictReader((run/'sample_manifest.csv').open(newline='')));records=[json.loads(l) for l in (run/'predictions.jsonl').read_text().splitlines()];idx={(p['pair_id'],p['input_condition'],p['side']):p for p in records};triage={p['pair_id']:p for p in json.loads((root/'visual_triage.json').read_text())['pairs']};pairs=[]
 for row in manifest:
  p=row['pair_id'];a=idx[p,'joint','safe'];b=idx[p,'joint','unsafe'];t=idx[p,'text_only','pair'];ia=idx[p,'image_only','safe'];ib=idx[p,'image_only','unsafe'];q=a['parsed_prediction']+'/'+b['parsed_prediction'];v=triage[p]
  pairs.append(dict(pair_id=p,category=row['category'],text=row['text'],safe_joint=a['parsed_prediction'],unsafe_joint=b['parsed_prediction'],text_only=t['parsed_prediction'],safe_image_only=ia['parsed_prediction'],unsafe_image_only=ib['parsed_prediction'],safe_false_positive=a['parsed_prediction']=='Unsafe',unsafe_false_negative=b['parsed_prediction']=='Safe',invalid_joint='INVALID' in q,pair_correct=q=='Safe/Unsafe',quadrant=q,changed_from_text_safe=a['parsed_prediction']!=t['parsed_prediction'],changed_from_text_unsafe=b['parsed_prediction']!=t['parsed_prediction'],literal_risk_label_in_user_text=bool(re.search(r'\b(?:safe|unsafe)\b',row['text'],re.I)),visual_difference=v['visible_difference'],review_question=v['review_question'],review_flags=';'.join(v['flags'])))
 with (root/'pair_error_analysis.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(pairs[0]));w.writeheader();w.writerows(pairs)
 (root/'pair_error_analysis.json').write_text(json.dumps(pairs,indent=2))
 # Pair-cluster bootstrap supplements marginal Wilson intervals; never resample data for inference.
 rng=random.Random(20261105);draws=[]
 for _ in range(2000):
  ps=rng.choices(pairs,k=len(pairs));tp=sum(p['unsafe_joint']=='Unsafe' for p in ps);tn=sum(p['safe_joint']=='Safe' for p in ps);fp=sum(p['safe_joint']=='Unsafe' for p in ps);fn=len(ps)-tp
  draws.append({'joint_accuracy':(tp+tn)/(2*len(ps)),'unsafe_F1':2*tp/(2*tp+fp+fn) if 2*tp+fp+fn else None,'PairAcc':sum(p['pair_correct'] for p in ps)/len(ps)})
 bootstrap={k:[sorted(d[k] for d in draws)[50],sorted(d[k] for d in draws)[1949]] for k in draws[0]}
 summary={'pairs':len(pairs),'false_negative_pair_ids':[p['pair_id'] for p in pairs if p['unsafe_false_negative']],'false_positive_pair_ids':[p['pair_id'] for p in pairs if p['safe_false_positive']],
 'literal_label_leak_pairs':[p['pair_id'] for p in pairs if p['literal_risk_label_in_user_text']],'text_only_Unsafe_pairs':[p['pair_id'] for p in pairs if p['text_only']=='Unsafe'],
 'joint_changes_from_text':sum(p['changed_from_text_safe']+p['changed_from_text_unsafe'] for p in pairs),'joint_differs_across_images':sum(p['safe_joint']!=p['unsafe_joint'] for p in pairs),
 'pair_bootstrap':{'unit':'pair, two Joint sides kept together','seed':20261105,'draws':2000,'percentile95':bootstrap},
 'caveat':'Cross-condition prompts differ; disagreement is not a causal mediation estimate. Visual triage is unblinded assistant review, not human causal validation.'}
 (root/'research_audit.json').write_text(json.dumps(summary,indent=2))
 # Independent metric cross-check, and exact manifest/history/source preservation.
 metrics=json.loads(next(run.glob('metrics_*.json')).read_text())['overall'];assert metrics['joint_accuracy']['count']==sum((p['safe_joint']=='Safe')+(p['unsafe_joint']=='Unsafe') for p in pairs);assert metrics['pair_accuracy']['count']==sum(p['pair_correct'] for p in pairs)
 freeze=json.loads((root/'parser_freeze.json').read_text());assert hashlib.sha256(pathlib.Path('scripts/official_parser_v2.py').read_bytes()).hexdigest()==freeze['source_sha256'];assert hashlib.sha256((run/'sample_manifest.csv').read_bytes()).hexdigest()==freeze['manifest_sha256']
 for p,h in json.loads((root/'history_hashes.json').read_text()).items():assert hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()==h
 memory={}
 for directory in ['formal_unified','validation_official','formal_official']:
  r=root/directory;p=r/'memory_samples.jsonl'
  if not p.exists():continue
  samples=[json.loads(l) for l in p.read_text().splitlines()];values=[s['process_mib'] for s in samples if s.get('process_mib') is not None]
  memory[directory]={'samples':len(samples),'pid_attribution_missing':sum(s.get('process_mib') is None for s in samples),'errors':sum('error' in s for s in samples),'process_peak_mib':max(values,default=None),'device_upper_bound_peak_mib':max((s['device_upper_bound_mib'] for s in samples if 'device_upper_bound_mib' in s),default=None),'torch_allocated_peak_bytes':max((s['torch_allocated_bytes'] for s in samples if 'torch_allocated_bytes' in s),default=None),'torch_reserved_peak_bytes':max((s['torch_reserved_bytes'] for s in samples if 'torch_reserved_bytes' in s),default=None),'identity':json.loads((r/'gpu_identity.json').read_text())}
  if values:assert max(values)<=20480
 (root/'memory_audit.json').write_text(json.dumps(memory,indent=2));return summary
if __name__=='__main__':
 import sys
 print(json.dumps(analyze(sys.argv[1]),indent=2))
