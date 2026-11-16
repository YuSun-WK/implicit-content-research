import unittest

from scripts.run_inference import parse_output, process_gpu_mib, update_revision_metadata
from unittest.mock import patch
from pathlib import Path
import json
import tempfile


class ParseTests(unittest.TestCase):
    def test_unified_exact_label(self):
        self.assertEqual(parse_output(' Unsafe\n', 'unified'), ('Unsafe', 'ok'))
        self.assertEqual(parse_output('I think Unsafe', 'unified')[0], 'INVALID')

    def test_official_only_final_overall(self):
        raw = ('1. Intent Analysis: [Unsafe] <|/Intent|>\n'
               '4. Relationship Risk: [Unsafe] <|/Risk|>\n'
               '5. Overall: benign outcome. [Safe] <|/Overall|>')
        self.assertEqual(parse_output(raw, 'official_five_step'), ('Safe', 'ok'))

    def test_official_missing_or_ambiguous_final(self):
        self.assertEqual(parse_output('4. Risk: [Unsafe]', 'official_five_step')[0], 'INVALID')
        self.assertEqual(parse_output('5. Overall: [Safe] [Unsafe] <|/Overall|>', 'official_five_step')[0], 'INVALID')
        self.assertEqual(parse_output('5. Overall: [Unsafe]', 'official_five_step')[0], 'INVALID')

    @patch('scripts.run_inference.os.getpid', return_value=123)
    @patch('scripts.run_inference.subprocess.run')
    def test_process_gpu_monitor_ignores_other_users(self, run, getpid):
        run.return_value.stdout = '999, 41000\n123, 18000\n'
        self.assertEqual(process_gpu_mib('2'), 18000)
        self.assertIn('--query-compute-apps=pid,used_gpu_memory', run.call_args.args[0])

    def test_metadata_keeps_both_protocols_and_legacy(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp)/'model_revisions.json'
            path.write_text(json.dumps({'legacy': {'status': 'old'}}))
            update_revision_metadata(path, 'model', 'unified', {'revision': 'a', 'session_id': 'one'})
            update_revision_metadata(path, 'model', 'official_five_step', {'revision': 'a', 'session_id': 'two'})
            result = json.loads(path.read_text())
            self.assertEqual(result['legacy']['status'], 'old')
            self.assertEqual(set(result['runs']['model']), {'unified', 'official_five_step'})
            update_revision_metadata(path, 'model', 'unified', {'revision': 'b', 'session_id': 'three'})
            self.assertEqual(len(json.loads(path.read_text())['runs']['model']['unified']), 2)


if __name__ == '__main__':
    unittest.main()
