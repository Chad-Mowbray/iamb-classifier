import unittest
from ipclassifier.token_processors.compounds import Compounds
from ipclassifier.utils import DictsSingleton



class TestCompounds(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.dicts = DictsSingleton()
        cls.words = cls.dicts.words
        cls.lemmatizer = cls.dicts.lemmatizer
        cls.uk_us_dict = cls.dicts.uk_us_dict
        cls.regularize_dicts = cls.dicts.regularize_dicts


    def test_compound_not_found(self):
        c = Compounds("apple", self.words, self.lemmatizer, self.uk_us_dict, self.regularize_dicts)
        compound = c.find_compound_in_wordlist()
        self.assertIsNone(compound)

    def test_compound_moonfaced_intercepted(self):
        c = Compounds("moonfaced", self.words, self.lemmatizer, self.uk_us_dict, self.regularize_dicts)
        compound = c.find_compound_in_wordlist()
        self.assertIsNone(compound)

    def test_compound_lampshine(self):
        c = Compounds("lampshine", self.words, self.lemmatizer, self.uk_us_dict, self.regularize_dicts)
        compound = c.find_compound_in_wordlist()
        self.assertEqual(compound, ['lamp', 'shine'])  

    def test_compound_selfstarter(self):
        c = Compounds("self-starter", self.words, self.lemmatizer, self.uk_us_dict, self.regularize_dicts)
        compound = c.find_compound_in_wordlist()
        self.assertEqual(compound, ['self', 'starter'])  

    def test_compound_colourcoded(self):
        c = Compounds("colour-shine", self.words, self.lemmatizer, self.uk_us_dict, self.regularize_dicts)
        compound = c.find_compound_in_wordlist()
        self.assertEqual(compound, ['color', 'shine'])  


if __name__ == "__main__":
    unittest.main()