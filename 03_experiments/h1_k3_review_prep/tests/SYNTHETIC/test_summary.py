"""SYNTHETIC-only tests. No real review record is created or prefilled."""
import copy,datetime,json,pathlib,sys,tempfile,unittest
ROOT=pathlib.Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'scripts'))
from summarize_reviews import summarize,validate_export,adjudications,read_export
SCHEMA=json.loads((ROOT/'schema.json').read_text());STAMP='2026-01-01T00:00:00Z'
def fixtures():
 baseline=[];reviewers={};exports=[]
 for i in range(36):baseline.append({'pair_id':f'SYNTHETIC/pair{i}','category':f'SYNTHETIC/category{i%2}','labels':{'safe':'Safe','unsafe':'Unsafe'},'joint':{'safe':'Safe','unsafe':'Safe' if i<4 else 'Unsafe'},'candidate_11':i<11})
 for who in ['ReviewerA','ReviewerB']:
  singles=[];pairs=[];sr=[];pr=[]
  for i,b in enumerate(baseline):
   pid=b['pair_id']
   for side in ['safe','unsafe']:
    id=f'S-SYNTHETIC-{who}-{i}-{side}';singles.append({'id':id,'pair_id':pid,'side':side});r={k:[] if d['type']=='multi' else 'SYNTHETIC rationale' if d['type']=='text' else d['options'][0] for k,d in SCHEMA['stage1'].items()};r.update(reviewer_id=who,anonymous_sample_id=id,submitted_at=STAMP,judgment=b['labels'][side],premises_status='None_identified');sr.append(r)
   left='safe' if who=='ReviewerA' else 'unsafe';right='unsafe' if left=='safe' else 'safe';id=f'P-SYNTHETIC-{who}-{i}';pairs.append({'id':id,'pair_id':pid,'left_side':left,'right_side':right});r={k:'SYNTHETIC paired rationale' if d['type']=='text' else d['options'][0] for k,d in SCHEMA['stage2'].items()};r.update(reviewer_id=who,anonymous_pair_id=id,submitted_at=STAMP,left_judgment=b['labels'][left],right_judgment=b['labels'][right],contrast_supported='Yes');pr.append(r)
  reviewers[who]={'package_id':'SYNTHETIC-'+who,'singles':singles,'pairs':pairs}
  for stage,records in [(1,sr),(2,pr)]:exports.append((f'SYNTHETIC-{who}-{stage}.json',{'schema_version':SCHEMA['schema_version'],'package_id':'SYNTHETIC-'+who,'reviewer_id':who,'stage':stage,'export_kind':'final','reviewer_attestation':True,'exported_at':STAMP,'phase1_locked_at':STAMP,'records':records,'test_marker':'SYNTHETIC'}))
 return {'reviewers':reviewers,'baseline':baseline},exports
class SummaryTests(unittest.TestCase):
 def test_empty_stays_pending_no_thresholds(self):
  r,_=fixtures();s=summarize(r,SCHEMA,[]);self.assertEqual(s['status'],'HUMAN_REVIEW_PENDING');self.assertEqual(s['threshold_evaluation'],'NOT_EVALUATED');self.assertNotIn('original_full_36_metrics',s)
 def test_real_mode_rejects_synthetic(self):
  r,e=fixtures();s=summarize(r,SCHEMA,e,True);self.assertEqual(s['status'],'HUMAN_REVIEW_PENDING');self.assertEqual(len(s['validation_errors']),4)
 def test_independence_confirmation_required(self):
  r,e=fixtures();s=summarize(r,SCHEMA,e,False,allow_synthetic=True);self.assertEqual(s['status'],'HUMAN_REVIEW_PENDING');self.assertEqual(s['independence_confirmation'],'PENDING_COORDINATOR_CONFIRMATION')
 def test_orientation_alignment_and_preserved_thresholds(self):
  r,e=fixtures();s=summarize(r,SCHEMA,e,True,allow_synthetic=True);self.assertEqual(s['status'],'SYNTHETIC_TEST_ONLY');self.assertEqual(s['pair_side_aligned_agreement']['rate'],1);self.assertEqual(s['investment_count_rules']['general']['observed_errors'],4);self.assertTrue(s['investment_count_rules']['general']['count_condition_met']);self.assertEqual(s['investment_count_rules']['special_11']['denominator'],11);self.assertEqual(s['investment_count_rules']['special_11']['required'],6);self.assertFalse(s['automatic_gpu_execution'])
 def test_no_lowering_six_of_eleven_or_four_errors(self):
  r,e=fixtures();r['baseline'][3]['joint']['unsafe']='Unsafe'
  for _,ex in e:
   if ex['stage']==2:
    for row in ex['records'][5:11]:row['contrast_supported']='No'
  s=summarize(r,SCHEMA,e,True,allow_synthetic=True);self.assertFalse(s['investment_count_rules']['general']['count_condition_met']);self.assertEqual(s['investment_count_rules']['special_11']['observed'],5);self.assertFalse(s['investment_count_rules']['special_11']['count_condition_met'])
 def test_exactly_six_of_eleven_is_the_boundary(self):
  r,e=fixtures()
  for _,ex in e:
   if ex['stage']==2:
    for row in ex['records'][6:11]:row['contrast_supported']='No'
  s=summarize(r,SCHEMA,e,True,allow_synthetic=True);self.assertEqual(s['investment_count_rules']['special_11']['observed'],6);self.assertTrue(s['investment_count_rules']['special_11']['count_condition_met'])
 def test_four_errors_in_one_category_is_not_enough(self):
  r,e=fixtures()
  for b in r['baseline']:b['category']='SYNTHETIC/one-category'
  s=summarize(r,SCHEMA,e,True,allow_synthetic=True);self.assertEqual(s['investment_count_rules']['general']['observed_errors'],4);self.assertFalse(s['investment_count_rules']['general']['count_condition_met'])
 def test_missing_duplicate_and_wrong_stage_are_errors(self):
  r,e=fixtures()
  for change in ['missing','duplicate','wrong']:
   x=copy.deepcopy(e)
   if change=='missing':x[0][1]['records'].pop()
   elif change=='duplicate':x[0][1]['records'].append(copy.deepcopy(x[0][1]['records'][0]))
   else:x[0][1]['stage']=2
   s=summarize(r,SCHEMA,x,True,allow_synthetic=True);self.assertEqual(s['status'],'HUMAN_REVIEW_PENDING');self.assertTrue(s['validation_errors'])
 def test_duplicate_exports_never_select_latest(self):
  r,e=fixtures();s=summarize(r,SCHEMA,[*e,e[0]],True,allow_synthetic=True);self.assertEqual(s['status'],'HUMAN_REVIEW_PENDING');self.assertTrue(s['validation_errors'])
 def test_underdetermined_and_disagreements_retained(self):
  r,e=fixtures();e[0][1]['records'][0]['judgment']='Underdetermined';s=summarize(r,SCHEMA,e,True,allow_synthetic=True);self.assertEqual(len(s['single_disagreements']),1);self.assertEqual(s['reviewer_distributions']['ReviewerA']['underdetermined_sides'],1);self.assertEqual(s['single_raw_agreement_including_U']['total'],72)
 def test_adjudication_requires_explicit_revision_chain(self):
  r,e=fixtures();a={'event_id':'SYNTHETIC-event1','human_adjudicator_id':'SYNTHETIC-human','pair_id':'SYNTHETIC/pair0','stage':1,'side':'safe','judgment':'Safe','rationale':'SYNTHETIC reason','created_at':STAMP};b=dict(a,event_id='SYNTHETIC-event2',judgment='Underdetermined')
  with self.assertRaises(ValueError):adjudications([a,b],r['baseline'])
  b['supersedes']=a['event_id'];out=adjudications([a,b],r['baseline']);self.assertEqual(out[1,'SYNTHETIC/pair0','safe']['event_id'],b['event_id'])
 def test_ui_csv_rehydrates_same_json_payload(self):
  folder=ROOT/'tests/SYNTHETIC/generated';j=json.loads((folder/'synthetic_ui_export.json').read_text());c=read_export(folder/'synthetic_ui_export.csv');self.assertTrue(c['exported_at']);self.assertTrue(j['exported_at']);c.pop('exported_at');j.pop('exported_at');self.assertEqual(c,j)
 def test_multiselect_quotes_and_newlines_roundtrip(self):
  folder=ROOT/'tests/SYNTHETIC/generated';j=json.loads((folder/'synthetic_ui_stage1.json').read_text());c=read_export(folder/'synthetic_ui_stage1.csv');self.assertTrue(c['exported_at']);self.assertTrue(j['exported_at']);c.pop('exported_at');j.pop('exported_at');self.assertEqual(c,j);self.assertEqual(c['records'][0]['missing_premises'],['Authorization','Consent']);self.assertIn('\n',c['records'][0]['rationale'])
if __name__=='__main__':unittest.main()
