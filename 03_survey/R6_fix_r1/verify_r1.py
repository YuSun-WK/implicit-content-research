"""Historical R6-Fix-R1 checks, compatible with 49-key R1 and 50-key integration.

For CURRENT release verification also run R6_final_integration/verify_final.py.
No source or model experiments are performed here.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
DRAFT = ROOT / '03_survey/R5_full_draft'
text = (DRAFT / 'Survey_Full_Draft.md').read_text()
bib = (DRAFT / 'references.bib').read_text()
body, reference_list = text.split('# 参考文献\n', 1)
scientific_body = body.split('<a id="appendix-a">', 1)[0]

def citekeys(value):
    return set(re.findall(r'(?<![\w])@([A-Za-z][\w-]+)', value))

entries = re.findall(r'^@\w+\s*\{\s*([^,\s]+)\s*,', bib, re.M)
keys = set(entries)
expected_keys = 50 if 'mao2025pragmatic' in keys else 49
assert len(keys) == len(entries) == expected_keys, 'Bib key count or duplication'
assert citekeys(scientific_body) == keys, 'Main text/Bib mismatch'
assert citekeys(body) == keys, 'Appendix/Bib mismatch'
manual = re.findall(r'^\d+\. \*\*([^*]+)\*\*', reference_list, re.M)
assert len(manual) == len(set(manual)) == expected_keys and set(manual) == keys
inventory = body.split('# 附录B ', 1)[1]
inventory_keys = re.findall(r'@([\w-]+)', inventory)
assert len(inventory_keys) == len(set(inventory_keys)) == expected_keys
assert set(inventory_keys) == keys
mapping = (DRAFT / 'Citation_Key_Mapping.md').read_text()
assert set(re.findall(r'`([\w-]+)`', mapping)) >= keys
for table in (DRAFT / 'tables').glob('T*.md'):
    assert citekeys(table.read_text()) <= keys, f'Missing table key: {table}'
    rows = [x for x in table.read_text().splitlines() if x.startswith('|')]
    widths = {x.count('|') for x in rows}
    assert len(widths) <= 1, f'Inconsistent Markdown table width: {table}'

assert re.findall(r'^# ([1-9]) ', text, re.M) == list('123456789')
assert '../R6_fix/R6Fix_Public_Code_Evidence_Index.md' not in body
for repo in ('leeyejin1231/RV-HATE', 'Shu-Wan/cadet', 'DUTIR-YSQ/MultiMM',
             'ZhengL00/MGMCF', 'sljgkjhwe/MCIB', 'Tunanzzz/Meerkat-VL'):
    assert re.search(r'https://github\.com/' + re.escape(repo)
                     + r'/blob/[0-9a-f]{40}/[^)]+#L\d+-L\d+', body), repo
for stale in ('1523', '1453', '16,258', '16258', 'contrast **244**',
              '该实现断言仍需公开固定版本', '公开实现风险待固定版本'):
    assert stale not in body, stale
    for name in ('T3_Coded_Language.md', 'T5_Multimodal_Meaning.md',
                 'T6_Multimodal_Safety.md', 'T7_Method_Families.md'):
        assert stale not in (DRAFT / 'tables' / name).read_text(), (name, stale)

# Brace balance is structural checking, not a BibTeX parser/style compilation.
balance = 0
for char in re.sub(r'\\[{}]', '', bib):
    balance += (char == '{') - (char == '}')
    assert balance >= 0, 'Unexpected closing brace in BibTeX'
assert balance == 0, 'Unbalanced BibTeX braces'
assert '正式论文[第8页Figure5]' in scientific_body
assert 'Qwen2.5-VL-32B' in scientific_body
assert '本轮正式PDF端点超时' not in scientific_body
t6 = (DRAFT / 'tables/T6_Multimodal_Safety.md').read_text()
assert '本轮正式PDF图题复核仍O' not in t6
assert '第8／39页' in t6
assert 'b38dc2e84d20899132125338b3ef8d31f54873660c2562c281c4d992c1f96aa8' in t6
print(f'PASS: main text/Bib/manual references/inventory = {expected_keys} unique keys')
print('PASS: table keys and widths; nine chapters; six immutable public source groups')
print('PASS: stale private-only code references and unpinned release integers removed')
print('PASS: Gate D official PDF page/model/denominator citations synchronized')
print('LIMIT: no BibTeX compiler, publisher-field certification, rendering or model reproduction')
