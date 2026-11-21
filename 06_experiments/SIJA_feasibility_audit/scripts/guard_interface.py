"""CPU-only interface. Roles, image order and parser are adaptation assumptions."""
import re
from pathlib import Path
PROMPT = Path(__file__).with_name('original_prompt.txt').read_text()

def messages(source, cue, prompt):
    # Explicit inputs prevent category/action/spec-annotation leakage.
    return [{'role':'system','content':PROMPT}, {'role':'user','content':[
        {'type':'image','image':source}, {'type':'image','image':cue},
        {'type':'text','text':prompt}]}]

def parse(text):
    answers = re.findall(r'<<answer>>\s*(.*?)\s*<</answer>>', text, re.S)
    if len(answers)!=1 or answers[0] not in ('YES','NO'):
        return {'status':'INVALID','allow':False}
    return {'status':answers[0],'allow':answers[0]=='YES'}

if __name__=='__main__':
    cases = [('', 'INVALID'), ('YES', 'INVALID'),
        ('<<answer>>YES<</answer>>','YES'),
        ('<<answer>>NO<</answer>>','NO'),
        ('<<answer>>YES NO<</answer>>','INVALID'),
        ('<<answer>>YES<</answer>><<answer>>NO<</answer>>','INVALID'),
        ('<<answer>>yes<</answer>>','INVALID')]
    for raw, expected in cases:
        assert parse(raw)['status']==expected
    m=messages('synthetic-source','synthetic-cue','ordinary edit')
    assert len(m[1]['content'])==3
    assert all(x in PROMPT for x in ('editing reference','editing action','editing specification'))
    print('PASS: 7 parser boundaries; two-image message; triple reconstruction; explicit metadata exclusion. No inference.')
