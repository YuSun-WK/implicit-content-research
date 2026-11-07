import unittest

from scripts.run_inference import parse_output


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


if __name__ == '__main__':
    unittest.main()
