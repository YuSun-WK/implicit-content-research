"""Check real bundles, original-byte integrity and accidental information disclosure."""
import csv,hashlib,io,json,pathlib,re,sys,zipfile
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
from build_review import ROOT,anonymous_layout,sha,gitbytes,BASE,MANIFEST,PRED

def check():
 private=ROOT/'private';registry=json.loads((private/'registry.json').read_text());rows=list(csv.DictReader((private/'original_manifest.csv').open(newline='')));byid={r['pair_id']:r for r in rows};seed=bytes.fromhex(json.loads((private/'seeds.json').read_text())['root_seed']);assert anonymous_layout(rows,seed)==registry['reviewers'];schema=json.loads((ROOT/'schema.json').read_text());assert (private/'original_manifest.csv').read_bytes()==gitbytes(BASE,MANIFEST);assert (private/'original_predictions.jsonl').read_bytes()==gitbytes(BASE,PRED);preds=[json.loads(l) for l in (private/'original_predictions.jsonl').read_text().splitlines()];assert len(preds)==180;idx={(p['pair_id'],p['input_condition'],p['side']):p for p in preds};assert len(idx)==180
 for row in rows:
  for side in ['safe','unsafe']:
   for condition in ['joint','image_only']:
    prediction=idx[row['pair_id'],condition,side];assert prediction['image_hash']==row[side+'_sha256'];assert prediction['image_path']==row[side+'_hf_path'];assert prediction['model_revision']=='76892f9768ce828268265171f4bbc5dfb75eafc3'
  assert idx[row['pair_id'],'text_only','pair']['ground_truth'] is None
 expected_private=json.loads((private/'package_files.json').read_text());count=0
 assert len(rows)==len(byid)==36
 foreign=['pair_id','category','ground_truth','original_safe_label','original_unsafe_label','joint_safe','joint_unsafe','grade','is_fn','is_fp','is_attenuation','root_seed','safe_hf_path','unsafe_hf_path']
 expected_single={(r['pair_id'],side) for r in rows for side in ['safe','unsafe']};orientations={};hashes=[]
 for reviewer,mapping in registry['reviewers'].items():
  package=ROOT/'packages'/reviewer;js=(package/'materials.js').read_text();prefix='window.REVIEW_SCHEMA=';a,b=js[len(prefix):].split(';\nwindow.REVIEW_DATA=',1);s=json.loads(a);d=json.loads(b.rsplit(';',1)[0]);assert s==schema;assert set(d)=={'schema_version','reviewer_id','package_id','singles','pairs'};assert d['reviewer_id']==reviewer and d['package_id']==mapping['package_id']
  assert len(d['singles'])==72 and len(d['pairs'])==36;assert len({p['id'] for p in d['singles']})==72;assert len({p['id'] for p in d['pairs']})==36;assert {(p['pair_id'],p['side']) for p in mapping['singles']}==expected_single
  image_ids=set()
  for item,m in zip(d['singles'],mapping['singles']):
   assert set(item)=={'id','text','image'} and item['id']==m['id'] and item['image']==m['image'];row=byid[m['pair_id']];assert item['text']==row['text'];assert re.fullmatch(r'assets/[a-f0-9]{20}\.png',item['image']);p=package/item['image'];assert not p.is_symlink();digest=sha(p.read_bytes());assert digest==row[m['side']+'_sha256'];hashes.append(digest);image_ids.add(item['image']);count+=1
  assert len(image_ids)==72
  orientation=[]
  for item,m in zip(d['pairs'],mapping['pairs']):
   assert set(item)=={'id','text','left','right'};assert item['id']==m['id'] and item['left']==m['left'] and item['right']==m['right'];assert item['left']!=item['right'] and item['left'] in image_ids and item['right'] in image_ids;assert item['text']==byid[m['pair_id']]['text'];assert {m['left_side'],m['right_side']}=={'safe','unsafe'};orientation.append(m['left_side'])
  assert set(orientation)=={'safe','unsafe'};orientations[reviewer]={'safe_on_left':orientation.count('safe'),'unsafe_on_left':orientation.count('unsafe')}
  for stage in [1,2]:
   template=list(csv.DictReader((package/f'review_form_stage{stage}.csv').open(newline='')));assert len(template)==(72 if stage==1 else 36)
   for record in template:
    assert all(record[k]=='' for k in schema['stage'+str(stage)]);assert record['submitted_at']=='' and record['reviewer_attestation']==''
  # Contextual leakage checks: options Safe/Unsafe are permitted, sample-level answers are not.
  for key in foreign:assert '"'+key+'"' not in js
  for p in package.rglob('*'):
   assert not p.is_symlink()
   if not p.is_file():continue
   rel=str(p.relative_to(ROOT/'packages'));assert rel in expected_private and sha(p.read_bytes())==expected_private[rel]
   assert not re.search(r'(?:_safe|_unsafe|test/|category|prediction|grade|private)',str(p.relative_to(package)),re.I)
   if p.suffix not in ['.png']:
    text=p.read_text();assert not any(re.search(r'\b'+re.escape(c)+r'\b',text) for c in {r['category'] for r in rows});assert not any(pid in text for pid in byid);assert not any(row['safe_hf_path'] in text or row['unsafe_hf_path'] in text for row in rows);assert not re.search(r'https?://|wss?://|huggingface|ThinkingGuard|A6/B12/C18|H1_K2_',text,re.I)
    if p.name=='app.js':assert not re.search(r'\bfetch\s*\(|XMLHttpRequest|WebSocket|sendBeacon|serviceWorker',text)
    if p.name=='index.html':assert "connect-src 'none'" in text
  # No extra public files can sneak into an archive.
  allowed={'index.html','app.js','style.css','materials.js','GUIDE.md','review_form_stage1.csv','review_form_stage2.csv'}|image_ids
  assert {str(p.relative_to(package)) for p in package.rglob('*') if p.is_file()}==allowed
 a,b=registry['reviewers'].values();assert [(x['pair_id'],x['side']) for x in a['singles']]!=[(x['pair_id'],x['side']) for x in b['singles']];assert [x['pair_id'] for x in a['pairs']]!=[x['pair_id'] for x in b['pairs']]
 for path,digest in json.loads((private/'old_files_hashes.json').read_text()).items():assert sha(pathlib.Path(path).read_bytes())==digest
 image_records=json.loads((private/'image_integrity.json').read_text());assert len(image_records)==72 and all(x['decode'] and x['sha256']==x['expected_sha256'] and not x['metadata_identity_leak'] for x in image_records)
 for path in (ROOT/'artifacts').glob('*.zip'):
  with zipfile.ZipFile(path) as z:
   assert not z.testzip();assert all(not n.startswith('/') and '..' not in pathlib.PurePosixPath(n).parts and 'private' not in n for n in z.namelist())
   expected={k: v for k,v in expected_private.items() if path.name=='H1_K3_Review_Materials.zip' or k.startswith(path.stem.replace('H1_K3_','')+'/')}
   actual={n if path.name=='H1_K3_Review_Materials.zip' else path.stem.replace('H1_K3_','')+'/'+n:sha(z.read(n)) for n in z.namelist()};assert actual==expected
 report={'status':'PASS','preparation_state':'PREPARED_FOR_HUMAN_REVIEW','human_review_state':'HUMAN_REVIEW_PENDING','pairs':36,'unique_sides':72,'verified_original_images':72,'reviewer_asset_checks':count,'reviewers':2,'stage1_per_reviewer':72,'stage2_per_reviewer':36,'source_images_reused':sum(x['origin']=='verified_existing_file' for x in image_records),'source_images_downloaded':sum(x['origin']=='fixed_revision_download' for x in image_records),'reproducible_orders':True,'different_reviewer_orders':True,'left_right_contains_both_original_sides':True,'orientation_counts_private':True,'reversible_mapping_private_only':True,'verbatim_text':True,'initial_judgments_blank':True,'no_source_ids_gt_predictions_grades_in_public_materials':True,'no_external_network_resources':True,'old_source_files_unchanged':True,'zip_private_exclusion':True,'images_uploaded_to_GitHub':False,'notes':'Safe/Unsafe option strings are allowed; checks examine sample-level prefill and source identities. No human judgments were produced.'}
 (ROOT/'evidence/integrity_report.json').write_text(json.dumps(report,indent=2));(private/'orientation_checks.json').write_text(json.dumps(orientations,indent=2));print(json.dumps(report,indent=2));return report
if __name__=='__main__':check()
