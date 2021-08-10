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

    def test_ea_count(self):
        ss = SpellingSyllabifier("treat")
        self.assertEqual(ss.syllable_count, 1)

    def test_consonantal_y_count(self):
        ss = SpellingSyllabifier("yea")
        self.assertEqual(ss.syllable_count, 1)

    def test_final_ed_count(self):
        ss = SpellingSyllabifier("harbingered")
        self.assertEqual(ss.syllable_count, 3)

    def test_dipthong_and_vowel_count(self):
        ss = SpellingSyllabifier("galilaean")
        self.assertEqual(ss.syllable_count, 4)

    def test_y_and_2_vowels_count(self):
        ss = SpellingSyllabifier("yeoman")
        self.assertEqual(ss.syllable_count, 2)

    def test_oldfashioned_est_count(self):
        ss = SpellingSyllabifier("renewest")
        self.assertEqual(ss.syllable_count, 2)

    def test_ey_and_repeated_vowel_count(self):
        ss = SpellingSyllabifier("linsey-woolsey")
        self.assertEqual(ss.syllable_count, 4)

    def test_ey_and_repeated_vowel_count(self):
        ss = SpellingSyllabifier("raiment")
        self.assertEqual(ss.syllable_count, 2)

    def test_frighted(self):
        ss = SpellingSyllabifier("frighted")
        self.assertEqual(ss.syllable_count, 1)
        self.assertEqual(len(ss.tentative_phonemes), 2)
        

if __name__ == "__main__":
    unittest.main()