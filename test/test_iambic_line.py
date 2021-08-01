import unittest
from iambic_line_processors.iambic_line import IambicLine
from token_processors.sentencizer import Sentencizer
from token_processors.tokenizer import Tokenizer


class TestIambicLine(unittest.TestCase):

    def setUp(self):
        self.ibls = []
        for l in [
            "disceased to pass address the earth aspect\n", 
            "the expeditious pass address within\n", 
            "disceased to pass address the earth respect\n", 
            "abbreviated\n"
            "But we have left those gentle haunts to pass\n",
            "humanity itself the race to pass"
            ]:
            sentencizer = Sentencizer(l)
            lines = sentencizer.main()
            tokenizer = Tokenizer(lines)
            line_tokens = tokenizer.create_tokens()
            for line in line_tokens:
                iambic_line_tokens = IambicLine(line)
                self.ibls.append(iambic_line_tokens)

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


class TestIambicLineFromFile(unittest.TestCase):

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