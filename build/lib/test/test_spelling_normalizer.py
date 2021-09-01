import unittest
from ipclassifier.token_processors.spelling import SpellingNormalizer
from ipclassifier.utils import DictsSingleton



class TestSpellingNormalizer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.dicts = DictsSingleton()
        cls.uk_us_dict = cls.dicts.uk_us_dict
        cls.regularize_dicts = cls.dicts.regularize_dicts


    def test_apostrophe_tis(self):
        sn = SpellingNormalizer("'tis", self.uk_us_dict, self.regularize_dicts)
        self.assertEqual(sn.modernized_word, ["tis", True, 'initial'])

    def test_apostrophe_th(self):
        sn = SpellingNormalizer("th'", self.uk_us_dict, self.regularize_dicts)
        self.assertEqual(sn.modernized_word, ["the", True, 'final'])

    def test_apostrophe_s(self):
        sn = SpellingNormalizer("heav'n", self.uk_us_dict, self.regularize_dicts)
        self.assertEqual(sn.modernized_word, ["heaven", True, 'medial'])

    def test_whettinge(self):
        sn = SpellingNormalizer("whettinge", self.uk_us_dict, self.regularize_dicts)
        self.assertEqual(sn.modernized_word, ["whetting", False, ''])

    def test_battelyons(self):
        sn = SpellingNormalizer("battelyons", self.uk_us_dict, self.regularize_dicts)
        self.assertEqual(sn.modernized_word, ["battalions", False, ''])

    def test_asdfasdf(self):
        sn = SpellingNormalizer("asdfasdf", self.uk_us_dict, self.regularize_dicts)
        self.assertEqual(sn.modernized_word, [None, False, ''])

    def test_viewest(self):
        sn = SpellingNormalizer("viewest", self.uk_us_dict, self.regularize_dicts)
        self.assertEqual(sn.modernized_word, ["view", False, ''])   

    def test_renewest(self):
        sn = SpellingNormalizer("renewest", self.uk_us_dict, self.regularize_dicts)
        self.assertEqual(sn.modernized_word, ["renew", False, ''])    

    def test_colour(self):
        sn = SpellingNormalizer("colour", self.uk_us_dict, self.regularize_dicts)
        self.assertEqual(sn.modernized_word, ["color", False, ''])     


if __name__ == "__main__":
    unittest.main()