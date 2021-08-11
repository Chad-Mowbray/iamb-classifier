import unittest
from token_processors.phoneme_fsm import PhonemeFSM


class TestPhonemeFSM(unittest.TestCase):

    def test_old_spelling(self):
        fsm = PhonemeFSM('disceased')
        analyzed = fsm.final_phoneme_repr
        self.assertEqual(analyzed[0], ['D', 'IH0', 'Z', 'IY1', 'Z', 'D'])
        self.assertEqual(analyzed[1], ['D', 'IH0', 'Z', 'IY1', 'Z', 'EH0', 'D'])

    def test_basic_compound(self):
        fsm = PhonemeFSM("lamplit")
        analyzed = fsm.final_phoneme_repr
        self.assertEqual(analyzed, [['L', 'AE1', 'M', 'P', 'L', 'IH1', 'T']])

    def test_old_spelling_compound(self):
        fsm = PhonemeFSM("silver-smithes")
        analyzed = fsm.final_phoneme_repr
        self.assertEqual(analyzed, [['S', 'IH1', 'L', 'V', 'ER0', 'S', 'M', 'IH1', 'TH', 'S']])

    def test_dashed_compound(self):
        fsm = PhonemeFSM("sun-moon")
        analyzed = fsm.final_phoneme_repr
        self.assertEqual(analyzed, [['S', 'AH1', 'N', 'M', 'UW1', 'N']])  

    def test_regular_compound(self):
        fsm = PhonemeFSM("silversmiths")
        analyzed = fsm.final_phoneme_repr
        self.assertEqual(analyzed, [['S', 'IH1', 'L', 'V', 'ER0', 'S', 'M', 'IH1', 'TH', 'S']])

    def test_regular_compound_ed(self):
        fsm = PhonemeFSM("moonfaced")
        analyzed = fsm.final_phoneme_repr
        self.assertEqual(analyzed, [
            ['M', 'UW1', 'N', 'F', 'EY1', 'S', 'T'], 
            ['M', 'UW1', 'N', 'F', 'EY1', 'S', 'EH0', 'T'], 
        ])

    def test_elided_the(self):
        fsm = PhonemeFSM("th'")
        analyzed = fsm.final_phoneme_repr
        self.assertEqual(analyzed, [['DH', 'AH0'], ['DH', 'AH1'], ['DH', 'IY0'], ['DH']])
        


if __name__ == "__main__":
    unittest.main()