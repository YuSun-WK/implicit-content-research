#!/usr/bin/env python3
"""Audit TriggerBench CSVs without downloading images."""
import collections
import csv
import hashlib
import json
import pathlib
import re
import subprocess
import sys
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / 'data/manifests'
REV = '3ac26e778db94a282711f463f22ba6db99643bee'
API = 'https://huggingface.co/api/datasets/Sandy124/TriggerBench'
FIELDS = ['pair_id','split','category','index','text','safe_csv','unsafe_csv','safe_image_path_original','unsafe_image_path_original','safe_hf_path','unsafe_hf_path','valid','issues']

def get_json(url):
    with urllib.request.urlopen(url, timeout=60) as r:
        return json.load(r)

def fetch(path, target):
    target.parent.mkdir(parents=True, exist_ok=True)
    url = f'https://huggingface.co/datasets/Sandy124/TriggerBench/resolve/{REV}/{path}'
    tmp=target.with_suffix(target.suffix+'.partial')
    subprocess.run(['curl','--http1.1','-fL','--retry','10','--retry-all-errors','--retry-delay','2','--max-time','120','-sS',url,'-o',str(tmp)],check=True)
    tmp.replace(target)

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    meta=get_json(API)
    files={x['rfilename'] for x in meta['siblings']}
    csvs=sorted(x for x in files if x.endswith('.csv') and re.match(r'^(test|train)/text_',x))
    rows=[]; malformed=[]; counts=collections.Counter(); raw_texts=collections.defaultdict(set)
    for path in csvs:
        split=path.split('/')[0]
        m=re.fullmatch(r'(.+)_(safe|unsafe)\.csv',pathlib.Path(path).name)
        if not m: malformed.append({'file':path,'issue':'filename'});continue
        category,side=m.groups()
        target=OUT/'source_csv'/path
        if not target.exists(): fetch(path,target)
        with target.open(encoding='utf-8-sig',newline='') as f:
            reader=csv.DictReader(f)
            if reader.fieldnames != ['index','text','image_path','category']:
                malformed.append({'file':path,'issue':'header','found':reader.fieldnames})
            for n,row in enumerate(reader,2):
                if None in row or any(row.get(k) is None for k in ['index','text','image_path','category']):
                    malformed.append({'file':path,'line':n,'issue':'malformed_csv'});continue
                idx=row['index'].strip()
                if not idx: malformed.append({'file':path,'line':n,'issue':'empty_index'});continue
                # Preserve the source category and path; use the CSV filename as category authority.
                item=dict(row,split=split,side=side,category_key=category,csv_path=path,line=n,
                          pair_id=f'{split}/{category}/{idx}')
                rows.append(item);counts[f'{split}/{side}']+=1
                raw_texts[split].add(row['text'])
    grouped=collections.defaultdict(lambda:collections.defaultdict(list))
    for row in rows: grouped[row['pair_id']][row['side']].append(row)
    manifest=[]; invalid=[]; issue_counts=collections.Counter(); warning_counts=collections.Counter(); cat_counts=collections.Counter()
    for pid,sides in sorted(grouped.items()):
        split,cat,idx=pid.split('/')
        issues=[]
        if len(sides['safe'])!=1 or len(sides['unsafe'])!=1: issues.append('side_count')
        safe=sides['safe'][0] if sides['safe'] else None
        unsafe=sides['unsafe'][0] if sides['unsafe'] else None
        if safe and unsafe and safe['text']!=unsafe['text']: issues.append('text_mismatch')
        images={}; stems={}
        for side,row in [('safe',safe),('unsafe',unsafe)]:
            if row is None: continue
            original=row['image_path']
            basename=pathlib.PurePosixPath(original).name
            expected=f'{split}/images_{split}/{cat}/{basename}'
            images[side]=expected
            if expected not in files: issues.append(f'{side}_image_missing')
            if not original or original!=original.strip() or re.search(r'\s',original): issues.append(f'{side}_path_whitespace')
            mbase=re.fullmatch(r'(.+)_(safe|unsafe)\.png',basename)
            if not mbase or mbase.group(2)!=side: issues.append(f'{side}_path_suffix')
            elif mbase.group(1)!=idx: warning_counts[f'{side}_index_differs_from_image_filename']+=1
            stems[side]=mbase.group(1) if mbase else None
            if row['category'] and row['category'].lower().replace(' ','_')!=cat:
                warning_counts[f'{side}_category_annotation_differs_from_file']+=1
        if safe and unsafe and stems.get('safe')!=stems.get('unsafe'): issues.append('image_stem_mismatch_between_sides')
        rec=dict(pair_id=pid,split=split,category=cat,index=idx,text=safe['text'] if safe else (unsafe['text'] if unsafe else ''),
                 safe_csv=safe['csv_path'] if safe else '',unsafe_csv=unsafe['csv_path'] if unsafe else '',
                 safe_image_path_original=safe['image_path'] if safe else '',unsafe_image_path_original=unsafe['image_path'] if unsafe else '',
                 safe_hf_path=images.get('safe',''),unsafe_hf_path=images.get('unsafe',''),valid=not issues,issues=';'.join(issues))
        manifest.append(rec)
        if issues: invalid.append(rec)
        for x in issues:issue_counts[x]+=1
        if not issues:cat_counts[f'{split}/{cat}']+=1
    text_groups=collections.defaultdict(list)
    for x in manifest:
        text_groups[(x['split'],x['text'])].append(x['pair_id'])
    duplicates={s:sum(len(v)-1 for (sp,_),v in text_groups.items() if sp==s and len(v)>1) for s in ['train','test']}
    overlap=raw_texts['train'] & raw_texts['test']
    schema={'dataset':'Sandy124/TriggerBench','revision':meta['sha'],'columns':['index','text','image_path','category'],
            'pair_key':'split/category/index','label_source':'CSV filename safe/unsafe suffix; imagefolder label is only category',
            'image_mapping':'pair by split/category/index; map each side to {split}/images_{split}/{category_from_csv_filename}/{basename_from_original_image_path}',
            'source_paths_unchanged':True,'csv_files':csvs}
    audit={'csv_count':len(csvs),'csv_rows':dict(counts),'pair_count':len(manifest),'valid_pair_count':sum(x['valid'] for x in manifest),
           'valid_pairs_by_category':dict(cat_counts),'invalid_pair_count':len(invalid),'issues':dict(issue_counts),
           'warnings':dict(warning_counts),'malformed_rows':malformed,'duplicate_text_pairs_within_split':duplicates,'train_test_text_overlap_unique':len(overlap),
           'train_test_text_overlap_examples':sorted(overlap)[:10],
           'paper_counts_match':{'train_3864_rows':counts['train/safe']+counts['train/unsafe']==3864,
                                 'test_1736_rows':counts['test/safe']+counts['test/unsafe']==1736},
           'image_existence_method':'repository file listing only; bytes and duplicate hashes checked after selection'}
    for name,obj in [('dataset_schema.json',schema),('data_audit.json',audit)]:
        (OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2))
    for name,data in [('pair_manifest.csv',manifest),('invalid_pairs.csv',invalid)]:
        with (OUT/name).open('w',encoding='utf-8',newline='') as f:
            w=csv.DictWriter(f,fieldnames=FIELDS);w.writeheader();w.writerows(data)
    lines=['# TriggerBench CSV audit','',f"Revision: `{meta['sha']}`",f"CSV files: {len(csvs)}",f"Rows: {len(rows)}",f"Pairs: {len(manifest)}; valid: {audit['valid_pair_count']}; invalid: {len(invalid)}",'',
           '## Valid pairs by split/category','']+[f'- {k}: {v}' for k,v in sorted(cat_counts.items())]+['','## Issues','']+[f'- {k}: {v}' for k,v in sorted(issue_counts.items())]+['','## Warnings','']+[f'- {k}: {v}' for k,v in sorted(warning_counts.items())]+[
           f"- Train/Test exact text overlap: {len(overlap)} unique texts",f"- Repeated text pair IDs within split: {duplicates}",
           '- Image presence checks use repository filenames. Image byte integrity and exact image duplicates require downloaded image bytes.']
    (OUT/'data_audit.md').write_text('\n'.join(lines)+'\n')
    print(json.dumps(audit,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
