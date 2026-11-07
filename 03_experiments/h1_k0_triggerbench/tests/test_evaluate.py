import copy
import unittest

from scripts.evaluate import AuditError, evaluate, bootstrap_pair_difference


MODEL = 'example/model'
REV = 'fixed-revision'
MANIFEST = [{'pair_id': 'test/a/1', 'category': 'a', 'split': 'test'},
            {'pair_id': 'test/a/2', 'category': 'a', 'split': 'test'}]


def records():
    out = []
    predictions = {('1', 'safe'): 'Safe', ('1', 'unsafe'): 'Unsafe',
                   ('2', 'safe'): 'Unsafe', ('2', 'unsafe'): 'INVALID'}
    for pair in MANIFEST:
        idx = pair['pair_id'].rsplit('/', 1)[1]
        for condition, sides in [('joint', ('safe', 'unsafe')),
                                 ('text_only', ('pair',)),
                                 ('image_only', ('safe', 'unsafe'))]:
            for side in sides:
                pred = predictions.get((idx, side), 'Safe')
                if condition != 'joint':
                    pred = 'Safe'
                out.append({'pair_id': pair['pair_id'], 'category': 'a', 'split': 'test',
                            'side': side, 'input_condition': condition, 'protocol': 'unified',
                            'model_id': MODEL, 'model_revision': REV,
                            'ground_truth': side.capitalize() if condition == 'joint' else None,
                            'parsed_prediction': pred, 'parse_status': 'invalid' if pred == 'INVALID' else 'ok',
                            'raw_model_output': 'unparseable' if pred == 'INVALID' else pred,
                            'prompt_id': condition+'_v1', 'max_new_tokens': 32, 'inference_time': 1.0})
    return out


class EvaluateTests(unittest.TestCase):
    def test_metrics_and_invalid_policy(self):
        result = evaluate(records(), MANIFEST, MODEL, REV)
        m = result['overall']
        self.assertEqual(m['joint_accuracy']['value'], .5)
        self.assertEqual(m['pair_accuracy']['value'], .5)
        self.assertEqual(m['unsafe_f1'], .5)
        self.assertEqual(m['safe_false_positive_rate']['value'], .5)
        self.assertEqual(m['unsafe_false_negative_rate']['value'], .5)
        self.assertEqual(m['parse_failure_rate']['value'], .25)
        self.assertEqual(m['quadrants']['Safe/Unsafe'], 1)
        self.assertEqual(m['invalid_pairs'], 1)
        self.assertIsNotNone(m['pair_accuracy']['wilson95'])
        self.assertIn('text_only_joint_agreement', result['agreements'])
        self.assertNotIn('text_only_accuracy', result)
        self.assertIsNone(bootstrap_pair_difference(result, result))

    def test_duplicate_rejected(self):
        rows = records()
        with self.assertRaisesRegex(AuditError, 'duplicate'):
            evaluate(rows+[copy.deepcopy(rows[0])], MANIFEST, MODEL, REV)

    def test_missing_rejected(self):
        with self.assertRaisesRegex(AuditError, 'missing'):
            evaluate(records()[:-1], MANIFEST, MODEL, REV)

    def test_invalid_mislabel_rejected(self):
        rows = records()
        rows[1]['parsed_prediction'] = 'INVALID'
        with self.assertRaisesRegex(AuditError, 'INVALID'):
            evaluate(rows, MANIFEST, MODEL, REV)

    def test_mixed_revision_rejected(self):
        rows = records()
        rows[0]['model_revision'] = 'other'
        with self.assertRaisesRegex(AuditError, 'mixed'):
            evaluate(rows, MANIFEST, MODEL, REV)

    def test_text_only_has_no_ground_truth(self):
        rows = records()
        next(x for x in rows if x['input_condition'] == 'text_only')['ground_truth'] = 'Safe'
        with self.assertRaisesRegex(AuditError, 'ground truth'):
            evaluate(rows, MANIFEST, MODEL, REV)


if __name__ == '__main__':
    unittest.main()
