import unittest
from iambic_line_processors import IambicLine
from dataprep import RawFileProcessor
from token_processors import Tokenizer

from utils import DictsSingleton


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
        is_valid_ip = self.ibls[2].is_valid_pattern
        self.assertTrue(is_valid_ip) 

    def test_stress_alteration(self):
        is_valid_ip = self.ibls[0].is_valid_pattern
        self.assertTrue(is_valid_ip)

    def test_stress_promotion(self):
        is_valid_ip = self.ibls[1].is_valid_pattern
        self.assertTrue(is_valid_ip)

    def test_too_short(self):
        is_valid_ip = self.ibls[3].is_valid_pattern
        self.assertFalse(is_valid_ip)
    
    def test_demote_stress(self):
        is_valid_ip = self.ibls[4].is_valid_pattern
        self.assertTrue(is_valid_ip)   

    def test_promote_polysyllabic_stress(self):
        is_valid_ip = self.ibls[5].is_valid_pattern
        self.assertTrue(is_valid_ip)    

    def test_heaven_optionally_1_syllable(self):
        is_valid_ip = self.ibls[6].is_valid_pattern
        self.assertTrue(is_valid_ip)    

    def test_non_initial_apostrophe(self):
        is_valid_ip = self.ibls[7].is_valid_pattern
        self.assertTrue(is_valid_ip)    

    def test_11_syllables(self):
        is_valid_ip = self.ibls[8].is_valid_pattern
        self.assertTrue(is_valid_ip)  

    def test_compound_false_alarm(self):
        is_valid_ip = self.ibls[9].is_valid_pattern
        self.assertTrue(is_valid_ip)   

    def test_compound_false_alarm_stress_alteration(self):
        is_valid_ip = self.ibls[10].is_valid_pattern
        self.assertTrue(is_valid_ip)    

    def test_optional_penultimate_stress_removal(self):
        is_valid_ip = self.ibls[11].is_valid_pattern
        self.assertTrue(is_valid_ip)  

    def test_optional_penultimate_stress_removal_with_stress_alteration(self):
        is_valid_ip = self.ibls[12].is_valid_pattern
        self.assertTrue(is_valid_ip)  

    def test_possessive_apostrophe_s_removed(self):
        is_valid_ip = self.ibls[13].is_valid_pattern
        self.assertTrue(is_valid_ip)    

    def test_anapest(self):
        is_valid_ip = self.ibls[14].is_valid_pattern
        self.assertFalse(is_valid_ip)    

    def test_multiple_reductions(self):
        is_valid_ip = self.ibls[15].is_valid_pattern
        self.assertTrue(is_valid_ip)    

    def test_multiple_elided_the(self):
        is_valid_ip = self.ibls[16].is_valid_pattern
        self.assertTrue(is_valid_ip)    

    def test_ed_ending(self):
        is_valid_ip = self.ibls[17].is_valid_pattern
        self.assertTrue(is_valid_ip)    

# class TestToIambicLineFromFile(unittest.TestCase):

#     def setUp(self):
#         self.ibls = []
#         with open("poems/test_poem.txt") as f:
#             contents = f.read()
#             sentencizer = Sentencizer(contents)
#             lines = sentencizer.main()
#             tokenizer = Tokenizer(lines)
#             line_tokens = tokenizer.create_tokens()
#             for line in line_tokens:
#                 iambic_line_tokens = IambicLine(line)
#                 self.ibls.append(iambic_line_tokens)

#     def test_exists(self):
#         self.assertTrue(self.ibls)
#         self.assertGreater(len(self.ibls), 1)

#         is_valid_ip = self.ibls[1].is_valid_pattern
#         self.assertTrue(is_valid_ip)


if __name__ == "__main__":
    unittest.main()