import unittest
from iambic_line_processors.iambic_line import IambicLine
from token_processors.sentencizer import Sentencizer
from token_processors.tokenizer import Tokenizer


class TestToIambicLine(unittest.TestCase):

    def setUp(self):
        self.ibls = []

        with open("test/test_data/basic_lines.txt") as f:
            contents = f.read()
            sentences = Sentencizer(contents).main()
            tokenizer = Tokenizer(sentences)
            line_tokens = tokenizer.create_tokens()
            for line in line_tokens:
                iambic_line = IambicLine(line)
                self.ibls.append(iambic_line)


        # self.ibls = []
        # for l in [
        #     "disceased to pass address the earth aspect\n", 
        #     "the expeditious pass address within\n", 
        #     "disceased to pass address the earth respect\n", 
        #     "abbreviated\n"
        #     "But we have left those gentle haunts to pass\n",
        #     "humanity itself the race to pass\n",
        #     "Both must alike from Heaven derive their light,\n",
        #     "Both must alike from Heav'n derive their light,\n"
        #     ]:
        #     sentencizer = Sentencizer(l)
        #     lines = sentencizer.main()
        #     tokenizer = Tokenizer(lines)
        #     line_tokens = tokenizer.create_tokens()
            # for line in line_tokens:
            #     iambic_line_tokens = IambicLine(line)
            #     self.ibls.append(iambic_line_tokens)

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
        self.assertFalse(is_valid_ip)  

    def test_compound_false_alarm(self):
        is_valid_ip = self.ibls[9].is_valid_pattern
        self.assertTrue(is_valid_ip)   

    def test_compound_false_alarm_stress_alteration(self):
        is_valid_ip = self.ibls[10].is_valid_pattern
        self.assertTrue(is_valid_ip)         


class TestToIambicLineFromFile(unittest.TestCase):

    def setUp(self):
        self.ibls = []
        with open("poems/test_poem.txt") as f:
            contents = f.read()
            sentencizer = Sentencizer(contents)
            lines = sentencizer.main()
            tokenizer = Tokenizer(lines)
            line_tokens = tokenizer.create_tokens()
            for line in line_tokens:
                iambic_line_tokens = IambicLine(line)
                self.ibls.append(iambic_line_tokens)

    def test_exists(self):
        self.assertTrue(self.ibls)
        self.assertGreater(len(self.ibls), 1)

        is_valid_ip = self.ibls[1].is_valid_pattern
        self.assertTrue(is_valid_ip)


if __name__ == "__main__":
    unittest.main()