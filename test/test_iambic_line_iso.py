import unittest
from unittest.mock import MagicMock
from iambic_line_processors.iambic_line import IambicLine




class TestIambicLineIso(unittest.TestCase):


    def test_demote_compound_stress_unchanged(self):
        """
        Both deregulatory Heav'n their light,
        """
        il = IambicLine("", DEV=True)
        m = MagicMock()
        il.check_validity_and_continue = m.check_validity_and_continue
        il.unique_dict_of_realized_stress_patterns = {
            (1, 0, 1, 0, 0, 2, 0, 0, 1, 1): [([1], [0, 1, 0, 0, 2, 0], [0], [1], [1])],
            (1, 0, 1, 0, 0, 2, 0, 1, 1, 1): [([1], [0, 1, 0, 0, 2, 0], [1], [1], [1])]
            }
        # il.current_state = 1
        il.demote_compound_stress()
        m.check_validity_and_continue.assert_called()
        m.check_validity_and_continue.assert_called_with(
            [([1], [0, 1, 0, 0, 2, 0], [0], [1], [1]), 
            ([1], [0, 1, 0, 0, 2, 0], [1], [1], [1])]
            )
    

    def test_demote_compound_stress(self):
        """
        Sees his own face, self-slain Humanity
        """
        il = IambicLine("", DEV=True)
        m = MagicMock()
        il.check_validity_and_continue = m.check_validity_and_continue
        il.unique_dict_of_realized_stress_patterns = {
            (1, 0, 1, 1, 1, 1, 0, 1, 0, 0): [([1], [0], [1], [1], [1, 1], [0, 1, 0, 0])],
            (1, 1, 1, 1, 1, 1, 0, 1, 0, 0): [([1], [1], [1], [1], [1, 1], [0, 1, 0, 0])]
            }
        # il.current_state = 1
        il.demote_compound_stress()
        m.check_validity_and_continue.assert_called()
        m.check_validity_and_continue.assert_called_with([
            ([1], [0], [1], [1], [2, 1], [0, 1, 0, 0]), 
            ([1], [0], [1], [1], [1, 2], [0, 1, 0, 0]), 
            ([1], [0], [1], [1], [1, 1], [0, 1, 0, 0]), 
            ([1], [1], [1], [1], [2, 1], [0, 1, 0, 0]), 
            ([1], [1], [1], [1], [1, 2], [0, 1, 0, 0]), 
            ([1], [1], [1], [1], [1, 1], [0, 1, 0, 0])
            ])



    def test_demote_monosyllable_stress(self):
        """
        Sees his own face, self-slain Humanity,
        """
        il = IambicLine("", DEV=True)
        m = MagicMock()
        il.check_validity_and_continue = m.check_validity_and_continue
        il.unique_dict_of_realized_stress_patterns = {
            (1, 0, 1, 1, 1, 1, 0, 1, 0, 0): [([1], [0], [1], [1], [1, 1], [0, 1, 0, 0])],
            (1, 0, 1, 1, 1, 2, 0, 1, 0, 0): [([1], [0], [1], [1], [1, 2], [0, 1, 0, 0])],
            (1, 0, 1, 1, 2, 1, 0, 1, 0, 0): [([1], [0], [1], [1], [2, 1], [0, 1, 0, 0])],
            (1, 1, 1, 1, 1, 1, 0, 1, 0, 0): [([1], [1], [1], [1], [1, 1], [0, 1, 0, 0])],
            (1, 1, 1, 1, 1, 2, 0, 1, 0, 0): [([1], [1], [1], [1], [1, 2], [0, 1, 0, 0])],
            (1, 1, 1, 1, 2, 1, 0, 1, 0, 0): [([1], [1], [1], [1], [2, 1], [0, 1, 0, 0])]
            }
        # il.current_state = 2
        il.demote_monosyllable_stress()
        m.check_validity_and_continue.assert_called()
        m.check_validity_and_continue.assert_called_with([
            ([1], [0], [1], [1], [1, 1], [0, 1, 0, 0]), 
            ([1], [0], [0], [1], [1, 1], [0, 1, 0, 0]), 
            ([0], [0], [1], [1], [1, 1], [0, 1, 0, 0]), 
            ([0], [0], [0], [1], [1, 1], [0, 1, 0, 0]), 
            ([1], [0], [1], [1], [1, 2], [0, 1, 0, 0]), 
            ([1], [0], [0], [1], [1, 2], [0, 1, 0, 0]), 
            ([0], [0], [1], [1], [1, 2], [0, 1, 0, 0]), 
            ([0], [0], [0], [1], [1, 2], [0, 1, 0, 0]),
            ([1], [0], [1], [1], [2, 1], [0, 1, 0, 0]), 
            ([1], [0], [0], [1], [2, 1], [0, 1, 0, 0]), 
            ([0], [0], [1], [1], [2, 1], [0, 1, 0, 0]), 
            ([0], [0], [0], [1], [2, 1], [0, 1, 0, 0]), 
            ([1], [1], [1], [1], [1, 1], [0, 1, 0, 0]), 
            ([1], [1], [0], [1], [1, 1], [0, 1, 0, 0]),
            ([0], [1], [1], [1], [1, 1], [0, 1, 0, 0]), 
            ([0], [1], [0], [1], [1, 1], [0, 1, 0, 0]), 
            ([1], [1], [1], [1], [1, 2], [0, 1, 0, 0]), 
            ([1], [1], [0], [1], [1, 2], [0, 1, 0, 0]), 
            ([0], [1], [1], [1], [1, 2], [0, 1, 0, 0]),
            ([0], [1], [0], [1], [1, 2], [0, 1, 0, 0]),
            ([1], [1], [1], [1], [2, 1], [0, 1, 0, 0]), 
            ([1], [1], [0], [1], [2, 1], [0, 1, 0, 0]), 
            ([0], [1], [1], [1], [2, 1], [0, 1, 0, 0]), 
            ([0], [1], [0], [1], [2, 1], [0, 1, 0, 0])
            ])      


    def test_demote_monosyllable_stress_unchanged(self):
        """
        Sees his own face, self-slain Humanity,
        """
        il = IambicLine("", DEV=True)
        m = MagicMock()
        il.check_validity_and_continue = m.check_validity_and_continue
        il.unique_dict_of_realized_stress_patterns = {
            (0, 1, 0, 0, 0, 0, 0, 0, 0, 0): [([0], [1], [0], [0], [0], [0], [0], [0], [0], [0])],

            }
        # il.current_state = 2
        il.demote_monosyllable_stress()
        m.check_validity_and_continue.assert_called()
        m.check_validity_and_continue.assert_called_with([])    


if __name__ == "__main__":
    unittest.main()