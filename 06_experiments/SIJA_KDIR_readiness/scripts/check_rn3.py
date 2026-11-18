"""Adversarial completeness regressions; fixtures do not represent human reviews."""
import json,subprocess,sys,hashlib
from pathlib import Path
from copy import deepcopy
from tempfile import TemporaryDirectory
from datetime import datetime,timezone,timedelta
from kdir_core import eligible,qualification_errors,grouped_metrics,CELLS
from validate_freeze import validate_groups
import jsonschema
ROOT=Path(__file__).parents[1]
schema=json.loads((ROOT/'review_schema.json').read_text());validator=jsonschema.Draft202012Validator(schema,format_checker=jsonschema.FormatChecker())
good=dict(group_id='CPU_ONLY',status='HUMAN_VERIFIED',source_reference='CPU fixture not actual evidence',risk_facts='CPU fixture',policy_clause='CPU fixture',ambiguity='',disagreements=[],review_disagreements_resolved=True,reviewer_ids=['CPU_R1','CPU_R2'],review_times_utc=['2000-01-01T00:00:00Z','2000-01-01T01:00:00+01:00'],er_executable_on_Is=True,no_other_violations=True,linkage_verified=True,er_instruction_origin='AUTHOR_EXECUTION_LOG',er_log_reference='CPU synthetic log reference',r_a_s={o:{k:'CPU fixture' for k in ('referent','action','specification','instruction_evidence')} for o in ('er','en')},four_cell_outcomes={c:'CPU fixture outcome' for c in CELLS},gold=dict(zip(CELLS,['ALLOW','BLOCK','ALLOW','ALLOW'])))
good.update(images={r:{'path':'CPU fixture only','sha256':'a'*64} for r in ('Iu','Is')},er_on_Is_evidence='CPU fixture',remaining_violations_evidence='CPU fixture')
assert eligible(good);validator.validate(good)

# Execute only the old pure eligibility function on the same adversarial record.
# This is a CPU regression, not a re-score of any historical model output.
import ast
old_source=subprocess.check_output(['git','-C',str(ROOT.parents[1]),'show','afe2ea86b949805fc26debd58e44bd19de80e537:06_experiments/SIJA_KDIR_readiness/scripts/kdir_core.py'],text=True)
old_node=next(n for n in ast.parse(old_source).body if isinstance(n,ast.FunctionDef) and n.name=='eligible')
old_ns={'CELLS':CELLS};exec(compile(ast.Module(body=[old_node],type_ignores=[]),'old_eligible_fixture','exec'),old_ns)
regression=deepcopy(good);regression['no_other_violations']='false'
assert old_ns['eligible'](regression) is True and eligible(regression) is False

cases=[]
for field in ('er_executable_on_Is','no_other_violations','linkage_verified','review_disagreements_resolved'):
    for value in ('false','true',False,1,0,[],None):
        g=deepcopy(good);g[field]=value;cases.append((field+':'+repr(value),g,True))
for value in ('not-a-time','2000-02-30T00:00:00Z','2000-01-01T00:00:00','2000-01-01T00:00:00+01:99',False,''):
    g=deepcopy(good);g['review_times_utc'][0]=value;cases.append(('invalid time',g,True))
g=deepcopy(good);g['review_times_utc'][0]=(datetime.now(timezone.utc)+timedelta(days=2)).isoformat();cases.append(('future timestamp',g,False))
g=deepcopy(good);g['reviewer_ids']=['CPU_R1','CPU_R1'];cases.append(('duplicate reviewer',g,True))
g=deepcopy(good);g['review_times_utc']=g['review_times_utc'][:1];cases.append(('missing reviewer time',g,True))
for field in ('source_reference','risk_facts','policy_clause','er_log_reference','er_on_Is_evidence','remaining_violations_evidence'):
    g=deepcopy(good);g[field]='  ';cases.append(('missing evidence '+field,g,True))
g=deepcopy(good);del g['r_a_s']['er']['instruction_evidence'];cases.append(('missing er provenance',g,True))
g=deepcopy(good);g['four_cell_outcomes']['Is_er']=True;cases.append(('unwritten outcome',g,True))
g=deepcopy(good);g['er_instruction_origin']='RESEARCHER_DRAFT';cases.append(('draft cannot enter original track',g,True))
for value in (None,False,[],{'Iu':{'path':'fixture','sha256':'not-a-hash'}}):
    g=deepcopy(good);g['images']=value;cases.append(('missing image evidence',g,True))
for name,g,schema_reject in cases:
    assert not eligible(g),name
    assert qualification_errors(g),name
    assert grouped_metrics([g],[],'Direct-CP')['eligible_groups']==0,name
    if schema_reject:assert list(validator.iter_errors(g)),name
with TemporaryDirectory() as tmp:
    tmp=Path(tmp);groups=[]
    for i in range(32):
        g=deepcopy(good);g.update(group_id=f'CPU_{i}',split='dev' if i<8 else 'test',source_pair_cluster=f'CPU_PAIR_{i}',near_duplicate_cluster=f'CPU_NEAR_{i}',source_ids=[])
        g['images']={}
        for role in ('Iu','Is'):
            f=tmp/f'fixture-{i}-{role}.bin';raw=f'CPU byte fixture {i} {role}'.encode();f.write_bytes(raw);g['images'][role]={'path':str(f),'sha256':hashlib.sha256(raw).hexdigest()}
        groups.append(g)
    assert validate_groups(groups)['status']=='FROZEN'
    groups[0]['no_other_violations']='false'
    try:validate_groups(groups)
    except ValueError:pass
    else:raise AssertionError('Freeze admitted string false')
    source=tmp/'bad.json';source.write_text(json.dumps(groups));out=tmp/'must-not-freeze.json'
    r=subprocess.run([sys.executable,'-O',str(ROOT/'scripts/validate_freeze.py'),'--groups',str(source),'--output',str(out)],capture_output=True)
    assert r.returncode!=0 and not out.exists(),'python -O bypassed gate'
print(json.dumps({'status':'PASS','adversarial_records':len(cases),'checked_layers':['eligible','schema_with_format_checker','grouped_metrics','freeze','freeze_under_python_O'],'positive_control':'synthetic metadata only; no human activity attested','old_string_false_admitted':True,'fixed_string_false_admitted':False,'mechanism_inference':False}))
