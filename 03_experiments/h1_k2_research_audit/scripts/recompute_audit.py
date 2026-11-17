"""Independent CPU-only audit. Reads historical artifacts; never overwrites them."""
import argparse
import collections
import csv
import gzip
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import random
import re
import subprocess

COMMIT = '0a043abbf575d6b21f8d4095dbdfba7bad880465'
MODEL_REV = '76892f9768ce828268265171f4bbc5dfb75eafc3'

def metrics(pairs, index):
    n = len(pairs)
    safe = [index[p, 'joint', 'safe']['parsed_prediction'] for p in pairs]
    unsafe = [index[p, 'joint', 'unsafe']['parsed_prediction'] for p in pairs]
    tp, tn, fp = unsafe.count('Unsafe'), safe.count('Safe'), safe.count('Unsafe')
    fn = n - tp
    return {'n': n, 'tp': tp, 'tn': tn, 'fp': fp, 'fn': fn,
            'accuracy': (tp+tn)/(2*n), 'precision': tp/(tp+fp) if tp+fp else None,
            'recall': tp/n, 'fnr': fn/n, 'fpr': fp/n,
            'f1': 2*tp/(2*tp+fp+fn),
            'pairacc': sum(a == 'Safe' and b == 'Unsafe' for a,b in zip(safe,unsafe))/n}

def wilson(k,n):
    z=1.959963984540054; p=k/n; d=1+z*z/n
    c=(p+z*z/(2*n))/d; h=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/d
    return [max(0,c-h),min(1,c+h)]

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--repo',type=Path,default=Path(__file__).resolve().parents[3])
    ap.add_argument('--write',action='store_true',help='write only a new K2 evidence file')
    args=ap.parse_args(); repo=args.repo.resolve()
    exp=repo/'03_experiments/h1_k0_triggerbench'
    run=exp/'runs/h1_k1_20261117_060147'; u=run/'formal_unified'
    manifest=list(csv.DictReader((u/'sample_manifest.csv').open(encoding='utf-8',newline='')))
    predictions=[json.loads(l) for l in (u/'predictions.jsonl').read_text(encoding='utf-8').splitlines()]
    index={(p['pair_id'],p['input_condition'],p['side']):p for p in predictions}
    cond=[('joint','safe'),('joint','unsafe'),('text_only','pair'),('image_only','safe'),('image_only','unsafe')]
    assert len(manifest)==36 and len(index)==len(predictions)==180
    assert set(index)=={(m['pair_id'],c,s) for m in manifest for c,s in cond}
    for m in manifest:
        for c,s in cond:
            p=index[m['pair_id'],c,s]
            assert (p['model_id'],p['model_revision'],p['protocol'])==('Sandy124/ThinkingGuard-8B',MODEL_REV,'unified')
            assert p['split']==m['split']=='test' and p['category']==m['category']
            assert p['ground_truth']==(s.capitalize() if c=='joint' else None)
            match=re.fullmatch(r'\s*(Safe|Unsafe)\s*[.!]?\s*',p['raw_model_output'],re.I)
            assert match and match[1].capitalize()==p['parsed_prediction'] and p['parse_status']=='ok'
            if s!='pair':
                assert p['image_path']==m[s+'_hf_path'] and p['image_hash']==m[s+'_sha256']
            assert p['max_new_tokens']==32 and p['do_sample'] is False
    ids=[m['pair_id'] for m in manifest]; out=metrics(ids,index)
    original=json.loads((u/'metrics_Sandy124__ThinkingGuard-8B_unified_36.json').read_text(encoding='utf-8'))
    for new,old in [('accuracy','joint_accuracy'),('precision','unsafe_precision'),('recall','unsafe_recall'),('fnr','unsafe_false_negative_rate'),('fpr','safe_false_positive_rate'),('pairacc','pair_accuracy')]:
        assert abs(out[new]-original['overall'][old]['value'])<1e-12
        r=original['overall'][old]
        assert all(abs(a-b)<1e-12 for a,b in zip(wilson(r['count'],r['total']),r['wilson95']))
    assert abs(out['f1']-original['overall']['unsafe_f1'])<1e-12
    rng=random.Random(20261105)
    draws=[metrics(rng.choices(ids,k=len(ids)),index) for _ in range(2000)]
    out['bootstrap']={k:[sorted(x[k] for x in draws)[50],sorted(x[k] for x in draws)[1949]] for k in ['accuracy','f1','pairacc']}
    out['attenuation_ids']=[p for p in ids if index[p,'joint','unsafe']['parsed_prediction']=='Safe' and index[p,'image_only','unsafe']['parsed_prediction']=='Unsafe']
    out['memory']={}
    for directory in ['formal_unified','validation_official']:
        samples=[json.loads(l) for l in gzip.decompress((run/directory/'memory_samples.jsonl.gz').read_bytes()).decode().splitlines()]
        times=[s['time'] for s in samples]
        out['memory'][directory]={'samples':len(samples),'peak_process_mib':max(s.get('process_mib',0) or 0 for s in samples),'max_gap_seconds':max(b-a for a,b in zip(times,times[1:]))}
    source=exp/'scripts/official_parser_v2.py'
    spec=importlib.util.spec_from_file_location('frozen_parser',source)
    parser=importlib.util.module_from_spec(spec); spec.loader.exec_module(parser)
    official=[json.loads(l) for l in (run/'validation_official/predictions.jsonl').read_text(encoding='utf-8').splitlines()]
    out['official_labels']=[parser.parse(p['raw_model_output'])['prediction'] for p in official]
    assert out['official_labels']==['INVALID','INVALID','Unsafe','Unsafe']
    # Compare immutable Git blobs, not CRLF-converted checkout bytes.
    hashes=json.loads((repo/'03_experiments/h1_k2_research_audit/evidence/source_sha256.json').read_text(encoding='utf-8'))
    for p,h in hashes.items():
        b=subprocess.check_output(['git','show',COMMIT+':'+p],cwd=repo)
        assert hashlib.sha256(b).hexdigest()==h,p
    out['original_source_hashes_verified']=len(hashes)
    out['historical_metrics_match']=True
    if args.write:
        dest=repo/'03_experiments/h1_k2_research_audit/evidence/recompute_verification.json'
        dest.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(out,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
