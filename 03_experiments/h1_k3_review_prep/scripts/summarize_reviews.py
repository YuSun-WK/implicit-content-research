"""Human exports only. Never runs GPU or promotes assistant screening to human evidence."""
import os,argparse,collections,csv,datetime,hashlib,json,pathlib,shutil,uuid
ROOT=pathlib.Path(__file__).resolve().parents[1]
LABELS={'Safe','Unsafe','Underdetermined'}
def iso(value):
 if not isinstance(value,str) or not value:return False
 try:return datetime.datetime.fromisoformat(value.replace('Z','+00:00')).tzinfo is not None
 except ValueError:return False

def read_export(path):
 path=pathlib.Path(path)
 if path.suffix.lower()=='.json':return json.loads(path.read_text())
 if path.suffix.lower()!='.csv':raise ValueError('Only JSON/CSV exports are accepted')
 with path.open(newline='',encoding='utf-8-sig') as stream:rows=list(csv.DictReader(stream))
 if not rows:raise ValueError('Empty CSV')
 meta=['schema_version','package_id','stage','export_kind','reviewer_attestation','exported_at','phase1_locked_at','test_marker'];root={k:rows[0].get(k,'') for k in meta}
 for row in rows:
  if any(row.get(k,'')!=root[k] for k in meta):raise ValueError('Mixed export metadata in CSV')
 if not root.get('test_marker'):root.pop('test_marker',None)
 root['reviewer_id']=rows[0]['reviewer_id'];root['stage']=int(root['stage']);root['reviewer_attestation']=root['reviewer_attestation'].lower()=='true';root['records']=[{k:v for k,v in row.items() if k not in meta} for row in rows]
 for row in root['records']:
  if 'missing_premises' in row:row['missing_premises']=json.loads(row['missing_premises']) if row['missing_premises'] else []
 return root

def validate_export(export,registry,schema,allow_synthetic=False):
 permitted={'schema_version','package_id','reviewer_id','stage','export_kind','reviewer_attestation','exported_at','phase1_locked_at','records','test_marker'}
 if set(export)-permitted:raise ValueError('Unexpected export fields')
 if export.get('test_marker') and not allow_synthetic:raise ValueError('SYNTHETIC export prohibited in real review summary')
 reviewer=export.get('reviewer_id');stage=export.get('stage')
 if reviewer not in registry['reviewers'] or stage not in [1,2]:raise ValueError('Unknown reviewer or stage')
 layout=registry['reviewers'][reviewer]
 if export.get('package_id')!=layout['package_id'] or export.get('schema_version')!=schema['schema_version']:raise ValueError('Package/schema mismatch')
 if export.get('export_kind')!='final' or export.get('reviewer_attestation') is not True:raise ValueError('Draft or missing independent-human attestation')
 if not iso(export.get('exported_at')) or not iso(export.get('phase1_locked_at')):raise ValueError('Missing export/freeze timestamp')
 items=layout['singles' if stage==1 else 'pairs'];idfield='anonymous_sample_id' if stage==1 else 'anonymous_pair_id';expected={x['id'] for x in items};rows=export.get('records',[]);ids=[x.get(idfield) for x in rows]
 if len(ids)!=len(set(ids)):raise ValueError('Duplicate anonymous record')
 if set(ids)!=expected:raise ValueError(f'Missing/unexpected anonymous records: {len(expected-set(ids))} missing')
 for row in rows:
  if set(row)!={'reviewer_id',idfield,'submitted_at',*schema['stage'+str(stage)]}:raise ValueError('Unexpected or missing record fields')
  if row['reviewer_id']!=reviewer or not iso(row['submitted_at']):raise ValueError('Record reviewer/time mismatch')
  for k,definition in schema['stage'+str(stage)].items():
   value=row[k]
   if definition['type']=='multi':
    if not isinstance(value,list) or any(x not in definition['options'] for x in value):raise ValueError('Invalid multiselect')
   elif not isinstance(value,str) or (definition['required'] and not value.strip()):raise ValueError('Missing required human field: '+k)
   elif definition['type']=='select' and value not in definition['options']:raise ValueError('Invalid option: '+k)
  if stage==1 and row['premises_status']=='Missing' and not row['missing_premises'] and not row['other_premise'].strip():raise ValueError('Missing premise detail')
 return reviewer,stage

def metric(rows):
 n=len(rows);tp=sum(r['reference']=='Unsafe' and r['prediction']=='Unsafe' for r in rows);tn=sum(r['reference']=='Safe' and r['prediction']=='Safe' for r in rows);fp=sum(r['reference']=='Safe' and r['prediction']=='Unsafe' for r in rows);fn=sum(r['reference']=='Unsafe' and r['prediction']!='Unsafe' for r in rows);buckets=collections.defaultdict(list)
 for r in rows:buckets[r['pair_id']].append(r)
 complete=[v for v in buckets.values() if len(v)==2 and {r['side'] for r in v}=={'safe','unsafe'}]
 return {'sides':n,'complete_pairs':len(complete),'TP':tp,'TN':tn,'FP':fp,'FN':fn,'accuracy':(tp+tn)/n if n else None,'unsafe_F1':2*tp/(2*tp+fp+fn) if 2*tp+fp+fn else None,'PairAcc':sum(all(r['reference']==r['prediction'] for r in v) for v in complete)/len(complete) if complete else None}

def adjudications(events,baseline):
 current={};ids=set();allowed_pairs={b['pair_id'] for b in baseline}
 for event in events:
  if event.get('pair_id') not in allowed_pairs or event.get('stage') not in [1,2] or not event.get('event_id') or event['event_id'] in ids or not event.get('human_adjudicator_id') or not event.get('rationale','').strip() or not iso(event.get('created_at')):raise ValueError('Invalid human adjudication event')
  key=(event['stage'],event['pair_id'],event.get('side') if event['stage']==1 else None)
  if key in current and event.get('supersedes')!=current[key]['event_id']:raise ValueError('Repeated adjudication requires explicit supersedes; refusing silent overwrite')
  if event['stage']==1 and (event.get('side') not in ['safe','unsafe'] or event.get('judgment') not in LABELS):raise ValueError('Invalid adjudicated side judgment')
  if event['stage']==2 and (event.get('contrast_supported') not in ['Yes','No','Underdetermined'] or set(event.get('judgments',{}))!={'safe','unsafe'} or any(x not in LABELS for x in event['judgments'].values())):raise ValueError('Invalid adjudicated pair judgment')
  ids.add(event['event_id']);current[key]=event
 return current

def summarize(registry,schema,exports,confirm_independent=False,events=None,allow_synthetic=False):
 pending={'status':'HUMAN_REVIEW_PENDING','threshold_evaluation':'NOT_EVALUATED','next_stage_suggestion':None,'automatic_gpu_execution':False,'received_valid_exports':0,'required_exports':4,'validation_errors':[],'expected_per_reviewer':{'single_sides':72,'pairs':36}}
 loaded={}
 for source,export in exports:
  try:
   key=validate_export(export,registry,schema,allow_synthetic)
   if key in loaded:raise ValueError('Multiple versions for reviewer/stage; explicitly select one, do not overwrite')
   loaded[key]=export
  except (ValueError,KeyError,TypeError) as error:pending['validation_errors'].append({'source':source,'error':str(error)})
 pending['received_valid_exports']=len(loaded);pending['missing_exports']=[{'reviewer_id':who,'stage':stage} for who in registry['reviewers'] for stage in [1,2] if (who,stage) not in loaded]
 if pending['validation_errors'] or len(loaded)!=4:return pending
 for who in registry['reviewers']:
  if loaded[who,1]['phase1_locked_at']!=loaded[who,2]['phase1_locked_at']:pending['validation_errors'].append({'source':who,'error':'Stage freeze receipts differ'})
 if pending['validation_errors']:return pending
 if not confirm_independent:pending['independence_confirmation']='PENDING_COORDINATOR_CONFIRMATION';return pending
 who_a,who_b=list(registry['reviewers']);singles={};pairs={}
 for who,layout in registry['reviewers'].items():
  sr={r['anonymous_sample_id']:r for r in loaded[who,1]['records']};pr={r['anonymous_pair_id']:r for r in loaded[who,2]['records']};singles[who]={(x['pair_id'],x['side']):sr[x['id']] for x in layout['singles']};pairs[who]={}
  for x in layout['pairs']:
   r=pr[x['id']];pairs[who][x['pair_id']]={'row':r,'judgments':{x['left_side']:r['left_judgment'],x['right_side']:r['right_judgment']}}
 agreement=[];disagreements=[];phase_changes=[];consensus={};pair_consensus={};baseline={b['pair_id']:b for b in registry['baseline']};current=adjudications(events or [],registry['baseline'])
 for key,a in singles[who_a].items():
  b=singles[who_b][key];same=a['judgment']==b['judgment'];agreement.append((same,a['judgment']!='Underdetermined' and b['judgment']!='Underdetermined'))
  if not same:disagreements.append({'pair_id':key[0],'side':key[1],'reviewer_a':a['judgment'],'reviewer_b':b['judgment']})
  event=current.get((1,*key));label=event['judgment'] if event else a['judgment'] if same else None
  if label in ['Safe','Unsafe']:consensus[key]={'judgment':label,'origin':'human_adjudication' if event else 'two_reviewer_agreement'}
 for pid,entry in pairs[who_a].items():
  other=pairs[who_b][pid];a=entry['row'];b=other['row'];event=current.get((2,pid,None));same=a['contrast_supported']==b['contrast_supported'] and entry['judgments']==other['judgments']
  if event:pair_consensus[pid]={'contrast':event['contrast_supported'],'judgments':event['judgments'],'origin':'human_adjudication'}
  elif same:pair_consensus[pid]={'contrast':a['contrast_supported'],'judgments':entry['judgments'],'origin':'two_reviewer_agreement'}
  for who in [who_a,who_b]:
   for side in ['safe','unsafe']:
    old=singles[who][pid,side]['judgment'];new=pairs[who][pid]['judgments'][side]
    if old!=new:phase_changes.append({'reviewer_id':who,'pair_id':pid,'side':side,'stage1':old,'stage2':new})
 human_rows=[];errors=[]
 for (pid,side),judgment in consensus.items():
  b=baseline[pid];row={'pair_id':pid,'side':side,'prediction':b['joint'][side],'reference':judgment['judgment'],'reference_origin':judgment['origin']};human_rows.append(row)
  if row['prediction']!=row['reference']:errors.append(dict(row,category=b['category'],reviewer_a_rationale=singles[who_a][pid,side]['rationale'],reviewer_b_rationale=singles[who_b][pid,side]['rationale']))
 full=[{'pair_id':b['pair_id'],'side':side,'reference':b['labels'][side],'prediction':b['joint'][side]} for b in baseline.values() for side in ['safe','unsafe']]
 supported=[pid for pid,c in pair_consensus.items() if c['contrast']=='Yes' and set(c['judgments'].values())=={'Safe','Unsafe'}];subset=[r for r in full if r['pair_id'] in supported];subset_human=[dict(r,reference=pair_consensus[r['pair_id']]['judgments'][r['side']]) for r in subset]
 candidate_ids=[pid for pid,b in baseline.items() if b['candidate_11']];candidate_supported=[pid for pid in candidate_ids if consensus.get((pid,'unsafe'),{}).get('judgment')=='Unsafe' and pid in pair_consensus and pair_consensus[pid]['contrast']=='Yes' and pair_consensus[pid]['judgments']=={'safe':'Safe','unsafe':'Unsafe'}]
 categories={e['category'] for e in errors};general=len(errors)>=4 and len(categories)>=2;special=len(candidate_supported)>=6
 rates=lambda arr:{'agree':sum(arr),'total':len(arr),'rate':sum(arr)/len(arr) if arr else None}
 distributions={who:{'single_judgments':dict(collections.Counter(r['judgment'] for r in singles[who].values())),'determinate_sides':sum(r['judgment']!='Underdetermined' for r in singles[who].values()),'underdetermined_sides':sum(r['judgment']=='Underdetermined' for r in singles[who].values()),'pair_validity':dict(collections.Counter(x['row']['contrast_supported'] for x in pairs[who].values()))} for who in [who_a,who_b]}
 pair_disagreements=[{'pair_id':pid,'reviewer_a':pairs[who_a][pid],'reviewer_b':pairs[who_b][pid]} for pid in pairs[who_a] if pairs[who_a][pid]['row']['contrast_supported']!=pairs[who_b][pid]['row']['contrast_supported'] or pairs[who_a][pid]['judgments']!=pairs[who_b][pid]['judgments']]
 return {'status':'SYNTHETIC_TEST_ONLY' if allow_synthetic else 'HUMAN_REVIEW_COMPLETE_PENDING_RESEARCHER_DECISION','reviewer_distributions':distributions,'single_raw_agreement_including_U':rates([same for same,_ in agreement]),'single_both_determinate_agreement':rates([same for same,determinate in agreement if determinate]),'single_disagreements':disagreements,'pair_validity_agreement':rates([pairs[who_a][pid]['row']['contrast_supported']==pairs[who_b][pid]['row']['contrast_supported'] for pid in pairs[who_a]]),'pair_side_aligned_agreement':rates([pairs[who_a][pid]['judgments'][side]==pairs[who_b][pid]['judgments'][side] for pid in pairs[who_a] for side in ['safe','unsafe']]),'pair_disagreements':pair_disagreements,'phase1_to_phase2_changes':phase_changes,'original_full_36_metrics':metric(full),'stage1_human_consensus_metrics':metric(human_rows),'stage2_supported_pair_subset':{'pairs':len(supported),'pair_ids':supported,'original_GT_metrics':metric(subset),'human_pair_reference_metrics':metric(subset_human),'not_strict_causal_certification':True},'human_agreed_model_error_candidates':errors,'human_agreed_error_pairs':len({e['pair_id'] for e in errors}),'adjudication_events_preserved':events or [],'investment_count_rules':{'general':{'minimum_errors':4,'minimum_categories':2,'observed_errors':len(errors),'unit':'single-side model error; distinct pairs separately reported','observed_categories':len(categories),'count_condition_met':general},'special_11':{'required':6,'denominator':11,'observed':len(candidate_supported),'supported_ids':candidate_supported,'count_condition_met':special}},'credibility_requires_researcher_review':True,'next_stage_suggestion':'Researcher review of candidate count conditions and reasons; credibility is not judged by software; no scientific verdict or GPU is automatic','automatic_gpu_execution':False,'caveat':'Reviewer identities and independence are coordinator-attested, not established by file IDs. Raw disagreements remain even after adjudication. Investment count rules are not significance tests.'}

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--review',action='append',type=pathlib.Path,default=[]);p.add_argument('--confirm-independent-humans',action='store_true');p.add_argument('--adjudications',type=pathlib.Path);p.add_argument('--output-dir',type=pathlib.Path,default=ROOT/'private/summary');a=p.parse_args()
 output=a.output_dir.resolve()
 if not (output.is_relative_to((ROOT/'private').resolve()) or output.is_relative_to((ROOT/'results').resolve())):raise SystemExit('Real review summary must remain under private/ or results/, never the public package')
 registry=json.loads((ROOT/'private/registry.json').read_text());schema=json.loads((ROOT/'schema.json').read_text());events=[];exports=[];read_errors=[]
 if a.adjudications:
  try:events=[json.loads(l) for l in a.adjudications.read_text().splitlines() if l.strip()]
  except Exception as e:read_errors.append({'source':a.adjudications.name,'error':str(e)})
 for file in a.review:
  try:exports.append((file.name,read_export(file)))
  except Exception as e:read_errors.append({'source':file.name,'error':str(e)})
 try:result=summarize(registry,schema,[] if read_errors else exports,a.confirm_independent_humans,events)
 except (ValueError,KeyError,TypeError) as e:
  read_errors.append({'source':'adjudication/association','error':str(e)});result=summarize(registry,schema,[],False)
 result.setdefault('validation_errors',[]).extend(read_errors)
 if read_errors:result.update(status='HUMAN_REVIEW_PENDING',threshold_evaluation='NOT_EVALUATED',next_stage_suggestion=None)
 output.mkdir(parents=True,exist_ok=True,mode=0o700);os.chmod(output,0o700)
 stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'_'+uuid.uuid4().hex[:8];folder=output/stamp;folder.mkdir(parents=True,exist_ok=False,mode=0o700);received=folder/'received';received.mkdir(mode=0o700)
 receipts=[]
 for file in [*a.review,*([a.adjudications] if a.adjudications else [])]:
  if not file.is_file():
   receipts.append({'original_filename':file.name,'error':'FILE_MISSING'});continue
  data=file.read_bytes();digest=hashlib.sha256(data).hexdigest();target=received/(digest+file.suffix)
  if target.exists():
   if target.read_bytes()!=data:raise ValueError('Content-addressed input conflict')
  else:target.write_bytes(data)
  receipts.append({'original_filename':file.name,'SHA256':digest,'stored':target.name})
 (folder/'input_receipts.json').write_text(json.dumps(receipts,indent=2));(folder/'summary.json').write_text(json.dumps(result,ensure_ascii=False,indent=2));print(json.dumps({'status':result['status'],'summary_path':str(folder/'summary.json'),'automatic_gpu_execution':False}))
