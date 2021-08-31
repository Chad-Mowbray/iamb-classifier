import unittest
from ipclassifier.token_processors.phoneme_fsm import PhonemeFSM
from ipclassifier.utils import DictsSingleton


class TestPhonemeFSM(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.dicts = DictsSingleton()

    def test_old_spelling(self):
        fsm = PhonemeFSM('disceased', self.dicts)
        analyzed = fsm.final_phoneme_repr
        self.assertEqual(analyzed[0], ['D', 'IH0', 'Z', 'IY1', 'Z', 'D'])
        self.assertEqual(analyzed[1], ['D', 'IH0', 'Z', 'IY1', 'Z', 'EH0', 'D'])

    def test_basic_compound_intercepted(self):
        fsm = PhonemeFSM("lamplit", self.dicts)
        analyzed = fsm.final_phoneme_repr
        self.assertEqual(analyzed, [['AH1', 'AH0'], ['AH1', 'AH0']] )

    # def test_old_spelling_compound(self):
    #     fsm = PhonemeFSM("silver-smithes", self.dicts)
    #     analyzed = fsm.final_phoneme_repr
    #     self.assertEqual(analyzed, [['S', 'IH1', 'L', 'V', 'ER0', 'S', 'M', 'IH1', 'TH', 'S']])

    def test_dashed_compound(self):
        fsm = PhonemeFSM("sun-moon", self.dicts)
        analyzed = fsm.final_phoneme_repr
        self.assertEqual(analyzed, [['S', 'AH1', 'N', 'M', 'UW1', 'N']])  

    # def test_regular_compound(self):
    #     fsm = PhonemeFSM("silversmiths", self.dicts)
    #     analyzed = fsm.final_phoneme_repr
    #     self.assertEqual(analyzed, [['S', 'IH1', 'L', 'V', 'ER0', 'S', 'M', 'IH1', 'TH', 'S']])

    def test_regular_compound_ed(self):
        fsm = PhonemeFSM("moonfaced", self.dicts)
        analyzed = fsm.final_phoneme_repr
        self.assertEqual(analyzed, [
           ['AH1', 'AH0'], ['AH1', 'EH0', 'AH0'], ['AH1', 'AH0', 'AH0']
        ])

    def test_elided_the(self):
        fsm = PhonemeFSM("th'", self.dicts)
        analyzed = fsm.final_phoneme_repr
        self.assertEqual(analyzed, [['DH', 'AH0'], ['DH', 'AH1'], ['DH', 'IY0'], ['DH']])
        

if __name__ == "__main__":
    unittest.main()