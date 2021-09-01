import unittest
import os
from ipclassifier.dataprep import RawFileProcessor


class TestRawFileProcessor(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.correct = "Of Paradise so late their happy seat\n"
        prefix = os.path.join(os.path.dirname(__file__), "test_data")
        rfp = RawFileProcessor(os.path.join(prefix, "raw_files/raw_lines.txt"))
        cls.cleaned = rfp.cleaned_contents

    def test_remove_digits(self):
        self.assertEqual(self.cleaned[0], self.correct)
    
    def test_remove_double_dash(self):
        self.assertEqual(self.cleaned[1], self.correct)

    def test_remove_extra_spaces(self):
        self.assertEqual(self.cleaned[2], self.correct)

    def test_remove_tabs(self):
        self.assertEqual(self.cleaned[3], self.correct)

    def test_remove_punct_in_word(self):
        self.assertEqual(self.cleaned[4], self.correct)

    def test_remove_final_apostrophe(self):
        self.assertEqual(self.cleaned[5], self.correct)


if __name__ == "__main__":
    unittest.main()