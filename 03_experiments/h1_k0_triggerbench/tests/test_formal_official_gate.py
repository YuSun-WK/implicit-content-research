import unittest,tempfile,pathlib,json,hashlib
from scripts.run_inference import validate_official_gate
class FormalGateTests(unittest.TestCase):
 def test_failed_or_missing_validation_stops_before_model_load(self):
  with self.assertRaises(RuntimeError):validate_official_gate('official_five_step','v2',36,None)
  with self.assertRaises(RuntimeError):validate_official_gate('official_five_step','original',36,None)
  with tempfile.TemporaryDirectory() as d:
   p=pathlib.Path(d)/'decision.json';p.write_text(json.dumps({'passed':False,'coverage':.5}))
   with self.assertRaises(RuntimeError):validate_official_gate('official_five_step','v2',36,p)
 def test_exact_validated_source_required(self):
  with tempfile.TemporaryDirectory() as d:
   p=pathlib.Path(d)/'decision.json';data={'passed':True,'coverage':1,'parser_source_sha256':'wrong'};p.write_text(json.dumps(data))
   with self.assertRaises(RuntimeError):validate_official_gate('official_five_step','v2',36,p)
   data['parser_source_sha256']=hashlib.sha256(pathlib.Path('scripts/official_parser_v2.py').read_bytes()).hexdigest();p.write_text(json.dumps(data));validate_official_gate('official_five_step','v2',36,p)
  validate_official_gate('unified','original',36,None);validate_official_gate('official_five_step','v2',2,None)
