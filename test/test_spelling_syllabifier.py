import unittest
from token_processors.spelling_syllabify import SpellingSyllabifier


class TestSpellingSyllabifier(unittest.TestCase):

    def test_qu_count(self):
        ss = SpellingSyllabifier("quality")
        self.assertEqual(ss.syllable_count, 3)

    def test_ion_count(self):
        ss = SpellingSyllabifier("inspections")
        self.assertEqual(ss.syllable_count, 3)

    def test_ion_not_applied(self):
        ss = SpellingSyllabifier("sion")
        self.assertEqual(ss.syllable_count, 2)

    def test_ae_count(self):
        ss = SpellingSyllabifier("aeneid")
        self.assertEqual(ss.syllable_count, 3)

    def test_repeated_vowel_count(self):
        ss = SpellingSyllabifier("look")
        self.assertEqual(ss.syllable_count, 1)

    def test_ou_count(self):
        ss = SpellingSyllabifier("thought")
        self.assertEqual(ss.syllable_count, 1)

    def test_ey_count(self):
        ss = SpellingSyllabifier("linsey")
        self.assertEqual(ss.syllable_count, 2)

    def test_ie_count(self):
        ss = SpellingSyllabifier("pixie")
        self.assertEqual(ss.syllable_count, 2)

    



    def test_ey_and_repeated_vowel_count(self):
        ss = SpellingSyllabifier("linsey-woolsey")
        self.assertEqual(ss.syllable_count, 4)

if __name__ == "__main__":
    unittest.main()