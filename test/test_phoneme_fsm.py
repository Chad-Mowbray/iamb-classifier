import unittest
from token_processors.phoneme_fsm import PhonemeFSM


class TestPhonemeFSM(unittest.TestCase):

    def test_old_spelling(self):
        fsm = PhonemeFSM('disceased')
        analyzed = fsm.dispatch()
        self.assertEqual(analyzed, [['D', 'IH0', 'Z', 'IY1', 'Z', 'D']])

    def test_basic_compound(self):
        fsm = PhonemeFSM("lamplit")
        analyzed = fsm.dispatch()
        self.assertEqual(analyzed, [['L', 'AE1', 'M', 'P', 'L', 'IH1', 'T']])

    def test_old_spelling_compound(self):
        fsm = PhonemeFSM("silver-smithes")
        analyzed = fsm.dispatch()
        self.assertEqual(analyzed, [['S', 'IH1', 'L', 'V', 'ER0', 'S', 'M', 'IH1', 'TH', 'S']])

    def test_dashed_compound(self):
        fsm = PhonemeFSM("sun-moon")
        analyzed = fsm.dispatch()
        self.assertEqual(analyzed, [['S', 'AH1', 'N', 'M', 'UW1', 'N']])  


if __name__ == "__main__":
    unittest.main()