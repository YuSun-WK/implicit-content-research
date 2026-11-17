from run_guard import parse
from metrics import summarize,wilson,paired
assert not parse('YES')['valid_answer']
assert parse('<<answer>>NO<</answer>>')['valid_answer']
assert not parse('<<answer>>YES<</answer>><<answer>>NO<</answer>>')['valid_answer']
assert summarize([])['unsafe']['conditional_gap'] is None
row=dict(id='fixture',group='unsafe',review_status='MACHINE_DRAFT',policy_status='MATCH',gold='DENY',answer='YES',R='CORRECT',A='CORRECT',S='CORRECT',condition='natural')
assert summarize([row])['unsafe']['reviewed_n']==0
row['review_status']='HUMAN_VERIFIED'
assert summarize([row])['unsafe']['gap_n']==1
row['policy_status']='POLICY_MISMATCH'
assert summarize([row])['unsafe']['reviewed_n']==0
assert wilson(0,0) is None
assert abs(wilson(5,10)[0]-0.236593)<0.00001
print('PASS: parser ambiguity, unverified exclusion, policy exclusion, zero-denominator, Wilson fixture. Synthetic fixtures only.')
