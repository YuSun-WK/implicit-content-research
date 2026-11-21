from pathlib import Path
from tempfile import TemporaryDirectory
from copy import deepcopy
from kdir_core import *

def rejects(f):
    try:f()
    except ValueError:return
    raise AssertionError('Expected rejection')
with TemporaryDirectory() as t:
    a=Path(t)/'a';b=Path(t)/'b';a.write_bytes(b'CPU fixture A');b.write_bytes(b'CPU fixture B')
    kw=dict(group_id='fixture',cell_id='Iu_er',condition='Direct-CP',model={'id':'fixture','revision':'r1'},prompt='p1',policy='cp1',images=[{'role':'source','path':str(a)},{'role':'cue','path':str(b)}],request_text='harmless CPU test',preprocessing={'processor_revision':'r1','max_edge':512,'crop':False,'mode':'RGB','image_order':['source','cue']},decoding={'max_new_tokens':256,'do_sample':False},runtime={'transformers':'fixture'})
    _,key=build_manifest(**kw)
    for field,value in [('model',{'id':'fixture','revision':'r2'}),('prompt','p2'),('policy','cp2'),('request_text','other'),('decoding',{'max_new_tokens':512}),('preprocessing',{**kw['preprocessing'],'max_edge':256}),('runtime',{'transformers':'different'})]:
        altered=deepcopy(kw);altered[field]=value;assert build_manifest(**altered)[1]!=key
    altered=deepcopy(kw);altered['images'][1]['role']='target';rejects(lambda:build_manifest(**altered))
    a.write_bytes(b'changed actual bytes');assert build_manifest(**kw)[1]!=key
    ordered=deepcopy(kw);ordered['images']=[{'role':'source','path':str(b)},{'role':'cue','path':str(a)}];assert build_manifest(**ordered)[1]!=build_manifest(**kw)[1]
assert approved_input({'source_path':'x','request_text':'test'})['request_text']=='test'
rejects(lambda:approved_input({'source_path':'x','request_text':'test','category':'LEAK'}))
rejects(lambda:approved_input({'source_path':'x','request_text':'test','gold':'ALLOW'}))
assert parse('<answer>ALLOW</answer>','Direct-CP')['intent']=='NOT_APPLICABLE'
assert parse('<answer>UNKNOWN</answer>','Direct-CP')['status']=='UNKNOWN'
assert parse('<answer>DEFER</answer>','Direct-CP')['status']=='DEFER'
for raw in ['ALLOW','<<answer>>ALLOW<</answer>>','<answer>ALLOW</answer><answer>BLOCK</answer>','<answer></answer>']:
    assert parse(raw,'Direct-CP')['status']=='INVALID'
rejects(lambda:completed_keys([{'execution_status':'COMPLETED','id':'old','condition':'old'}]))
r={'execution_status':'COMPLETED','manifest_sha256':'a'*64};assert completed_keys([r])=={'a'*64};rejects(lambda:completed_keys([r,r]))
assert grouped_metrics([],[],'Direct-CP')['GAcc']['rate'] is None
fixture={'group_id':'g','status':'HUMAN_VERIFIED','reviewer_ids':['CPU_R1','CPU_R2'],'review_times_utc':['2000-01-01T00:00:00Z','2000-01-01T00:01:00Z'],'er_executable_on_Is':True,'no_other_violations':True,'linkage_verified':True,'gold':dict(zip(CELLS,['ALLOW','BLOCK','ALLOW','ALLOW']))}
fixture.update(images={r:{'path':'CPU fixture only','sha256':'a'*64} for r in ('Iu','Is')},er_on_Is_evidence='CPU fixture',remaining_violations_evidence='CPU fixture',source_reference='CPU synthetic source',risk_facts='CPU synthetic fact',policy_clause='CPU synthetic policy',ambiguity='',disagreements=[],review_disagreements_resolved=True,er_instruction_origin='AUTHOR_EXECUTION_LOG',er_log_reference='CPU fixture, not a real log',r_a_s={o:{k:'CPU synthetic evidence' for k in ('referent','action','specification','instruction_evidence')} for o in ('er','en')},four_cell_outcomes={c:'CPU synthetic outcome' for c in CELLS})
records=[dict(group_id='g',cell_id=c,condition='Direct-CP',status=fixture['gold'][c]) for c in CELLS]
assert grouped_metrics([fixture],records,'Direct-CP')['GAcc']['k']==1
records[0]['status']='DEFER';result=grouped_metrics([fixture],records,'Direct-CP');assert result['GAcc']['k']==0 and result['DirectionPairAcc']['k']==0 and result['output_status_counts']['DEFER']==1
fixture['status']='CODEX_DRAFT';assert grouped_metrics([fixture],records,'Direct-CP')['eligible_groups']==0
assert wilson(0,0) is None and abs(wilson(5,10)[0]-.236593)<.00001
print('PASS: CPU synthetic fixtures only. Manifest isolation (model/prompt/policy/images/order/preprocessing/decoding/runtime), whitelist, duplicate output, strict tags, UNKNOWN/DEFER/INVALID, N/A intent, group denominators, review gate and zero denominator. No safety inference.')

assert group_bootstrap([],[],'Direct-CP')['unsafe_allow'] is None
