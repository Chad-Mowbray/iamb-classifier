import unittest
from token_processors.phoneme_fsm import PhonemeFSM


class TestPhonemeFSM(unittest.TestCase):

    def test_old_spelling(self):
        fsm = PhonemeFSM('disceased')
        analyzed = fsm.final_phoneme_repr
        self.assertEqual(analyzed[0], ['D', 'IH0', 'Z', 'IY1', 'Z', 'D'])
        self.assertEqual(analyzed[1], ['D', 'IH0', 'Z', 'IY1', 'Z', 'EH0', 'D'])

    def test_basic_compound_intercepted(self):
        fsm = PhonemeFSM("lamplit")
        analyzed = fsm.final_phoneme_repr
        self.assertEqual(analyzed, [['AH1', 'AH0'], ['AH1', 'AH0']] )

    # def test_old_spelling_compound(self):
    #     fsm = PhonemeFSM("silver-smithes")
    #     analyzed = fsm.final_phoneme_repr
    #     self.assertEqual(analyzed, [['S', 'IH1', 'L', 'V', 'ER0', 'S', 'M', 'IH1', 'TH', 'S']])

    def test_dashed_compound(self):
        fsm = PhonemeFSM("sun-moon")
        analyzed = fsm.final_phoneme_repr
        self.assertEqual(analyzed, [['S', 'AH1', 'N', 'M', 'UW1', 'N']])  

    # def test_regular_compound(self):
    #     fsm = PhonemeFSM("silversmiths")
    #     analyzed = fsm.final_phoneme_repr
    #     self.assertEqual(analyzed, [['S', 'IH1', 'L', 'V', 'ER0', 'S', 'M', 'IH1', 'TH', 'S']])

    # for now...
    def test_regular_compound_ed(self):
        fsm = PhonemeFSM("moonfaced")
        analyzed = fsm.final_phoneme_repr
        self.assertEqual(analyzed, [
            ['AH1', 'AH0'], ['AH1', 'AH0', 'AH0', 'AH0']
        ])

    def test_elided_the(self):
        fsm = PhonemeFSM("th'")
        analyzed = fsm.final_phoneme_repr
        self.assertEqual(analyzed, [['DH', 'AH0'], ['DH', 'AH1'], ['DH', 'IY0'], ['DH']])
        


if __name__ == "__main__":
    unittest.main()