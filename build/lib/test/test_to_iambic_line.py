import unittest
from ipclassifier.iambic_line_processors import IambicLine
from ipclassifier.dataprep import RawFileProcessor
from ipclassifier.token_processors import Tokenizer
from ipclassifier.utils import DictsSingleton



class TestToIambicLine(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.dicts = DictsSingleton()

    def setUp(self):
        self.ibls = []
        sentences = RawFileProcessor("test/test_data/basic_lines.txt").cleaned_contents
        tokenizer = Tokenizer(sentences, self.dicts)
        line_tokens = tokenizer.create_tokens()
        for line in line_tokens:
            iambic_line = IambicLine(line)
            self.ibls.append(iambic_line)


    def test_simple_case(self):
        is_valid_ip = self.ibls[2]._is_valid_pattern
        self.assertTrue(is_valid_ip) 

    def test_stress_alteration(self):
        is_valid_ip = self.ibls[0]._is_valid_pattern
        self.assertTrue(is_valid_ip)

    def test_stress_promotion(self):
        is_valid_ip = self.ibls[1]._is_valid_pattern
        self.assertTrue(is_valid_ip)

    def test_too_short(self):
        is_valid_ip = self.ibls[3]._is_valid_pattern
        self.assertFalse(is_valid_ip)
    
    def test_demote_stress(self):
        is_valid_ip = self.ibls[4]._is_valid_pattern
        self.assertTrue(is_valid_ip)   

    def test_promote_polysyllabic_stress(self):
        is_valid_ip = self.ibls[5]._is_valid_pattern
        self.assertTrue(is_valid_ip)    

    def test_heaven_optionally_1_syllable(self):
        is_valid_ip = self.ibls[6]._is_valid_pattern
        self.assertTrue(is_valid_ip)    

    def test_non_initial_apostrophe(self):
        is_valid_ip = self.ibls[7]._is_valid_pattern
        self.assertTrue(is_valid_ip)    

    def test_11_syllables(self):
        is_valid_ip = self.ibls[8]._is_valid_pattern
        self.assertTrue(is_valid_ip)  

    def test_compound_false_alarm(self):
        is_valid_ip = self.ibls[9]._is_valid_pattern
        self.assertTrue(is_valid_ip)   

    def test_compound_false_alarm_stress_alteration(self):
        is_valid_ip = self.ibls[10]._is_valid_pattern
        self.assertTrue(is_valid_ip)    

    def test_optional_penultimate_stress_removal(self):
        is_valid_ip = self.ibls[11]._is_valid_pattern
        self.assertTrue(is_valid_ip)  

    def test_optional_penultimate_stress_removal_with_stress_alteration(self):
        is_valid_ip = self.ibls[12]._is_valid_pattern
        self.assertTrue(is_valid_ip)  

    def test_possessive_apostrophe_s_removed(self):
        is_valid_ip = self.ibls[13]._is_valid_pattern
        self.assertTrue(is_valid_ip)    

    def test_anapest(self):
        is_valid_ip = self.ibls[14]._is_valid_pattern
        self.assertFalse(is_valid_ip)    

    def test_multiple_reductions(self):
        is_valid_ip = self.ibls[15]._is_valid_pattern
        self.assertTrue(is_valid_ip)    

    def test_multiple_elided_the(self):
        is_valid_ip = self.ibls[16]._is_valid_pattern
        self.assertTrue(is_valid_ip)    

    def test_ed_ending(self):
        is_valid_ip = self.ibls[17]._is_valid_pattern
        self.assertTrue(is_valid_ip)    


if __name__ == "__main__":
    unittest.main()