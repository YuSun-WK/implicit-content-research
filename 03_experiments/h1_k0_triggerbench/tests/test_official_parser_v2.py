import unittest
from scripts.official_parser_v2 import parse,structure
class OfficialV2Tests(unittest.TestCase):
 def test_numbered_and_plain(self):
  for head in ('5. Overall:','Overall:'):
   for label in ('[Safe]','Unsafe','Verdict: Safe'):
    p=parse(head+' result. '+label+'. <|/Overall|>');self.assertEqual(p['status'],'ok')
 def test_implicit_boundary(self):
  p=parse('risk <|/Risk|>\nAnalyze the consistency between image and text content. Result. [Unsafe]. <|/Overall|>');self.assertEqual(p['prediction'],'Unsafe')
 def test_earlier_labels_ignored(self):
  self.assertEqual(parse('Intent: [Unsafe] <|/Intent|>\nOverall: [Safe]. <|/Overall|>')['prediction'],'Safe')
 def test_ambiguity_and_negation(self):
  for body in ('[Safe] [Unsafe]','Safe. But Unsafe.','not Unsafe.','[Safe]/[Unsafe]','Safe. Safe.','This is a safe activity.','"Safe"',''):
   self.assertEqual(parse('Overall: '+body+' <|/Overall|>')['prediction'],'INVALID',body)
 def test_termination_and_boundaries(self):
  for raw in ('Overall: Safe.','Safe. <|/Overall|>','Overall: Safe. <|/Overall|> more','Overall: Safe. <|/Overall|> <|/Overall|>','Overall: Safe.\nOverall: Unsafe. <|/Overall|>','risk <|/Risk|> Safe. <|/Overall|>'):
   self.assertEqual(parse(raw)['prediction'],'INVALID',raw)
 def test_structure_separate(self):
  raw='intent <|/Intent|>\n<|/Entity|>\nattributes <|/Attribute|>\nrisk <|/Risk|>\nOverall: Unsafe. <|/Overall|>'
  self.assertEqual(parse(raw)['prediction'],'Unsafe');self.assertFalse(structure(raw)['complete']);self.assertEqual(structure(raw)['steps']['Entity'],'empty')
  self.assertTrue(structure(raw.replace('<|/Entity|>','entities <|/Entity|>'))['complete'])
 def test_developer_fixtures(self):
  # Synthetic cases are frozen before the held-out model validation.
  self.assertEqual(parse('Overall: Result. [Unsafe]. Risk category is [Privacy]. <|/Overall|><|im_end|>')['prediction'],'Unsafe')

 def test_descriptive_safe_is_not_a_label(self):
  self.assertEqual(parse('Overall: [Result: a safe, appropriate grooming setup]. [Safe]. <|/Overall|>')['prediction'],'Safe')
