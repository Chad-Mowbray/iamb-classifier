import unittest
from unittest.mock import MagicMock
from ipclassifier.iambic_line_processors import IambicLine



class TestIambicLineIso(unittest.TestCase):

    def setUp(self):
        self.il = IambicLine("", DEV=True)
        self.m = MagicMock()
        self.il._check_validity_and_continue = self.m.check_validity_and_continue


    def test_demote_compound_stress_unchanged(self):
        """
        Both deregulatory Heav'n their light,
        """
        self.il._unique_dict_of_realized_stress_patterns = {
            (1, 0, 1, 0, 0, 2, 0, 0, 1, 1): [([1], [0, 1, 0, 0, 2, 0], [0], [1], [1])],
            (1, 0, 1, 0, 0, 2, 0, 1, 1, 1): [([1], [0, 1, 0, 0, 2, 0], [1], [1], [1])]
            }
        self.il._demote_compound_stress()
        self.m.check_validity_and_continue.assert_called()
        self.m.check_validity_and_continue.assert_called_with(
            [([1], [0, 1, 0, 0, 2, 0], [0], [1], [1]), 
            ([1], [0, 1, 0, 0, 2, 0], [1], [1], [1])]
            )
    

    def test_demote_compound_stress(self):
        """
        Sees his own face, self-slain Humanity
        """
        self.il._unique_dict_of_realized_stress_patterns = {
            (1, 0, 1, 1, 1, 1, 0, 1, 0, 0): [([1], [0], [1], [1], [1, 1], [0, 1, 0, 0])],
            (1, 1, 1, 1, 1, 1, 0, 1, 0, 0): [([1], [1], [1], [1], [1, 1], [0, 1, 0, 0])]
            }
        self.il._demote_compound_stress()
        self.m.check_validity_and_continue.assert_called()
        self.m.check_validity_and_continue.assert_called_with([
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
        self.il._unique_dict_of_realized_stress_patterns = {
            (1, 0, 1, 1, 1, 1, 0, 1, 0, 0): [([1], [0], [1], [1], [1, 1], [0, 1, 0, 0])],
            (1, 0, 1, 1, 1, 2, 0, 1, 0, 0): [([1], [0], [1], [1], [1, 2], [0, 1, 0, 0])],
            (1, 0, 1, 1, 2, 1, 0, 1, 0, 0): [([1], [0], [1], [1], [2, 1], [0, 1, 0, 0])],
            (1, 1, 1, 1, 1, 1, 0, 1, 0, 0): [([1], [1], [1], [1], [1, 1], [0, 1, 0, 0])],
            (1, 1, 1, 1, 1, 2, 0, 1, 0, 0): [([1], [1], [1], [1], [1, 2], [0, 1, 0, 0])],
            (1, 1, 1, 1, 2, 1, 0, 1, 0, 0): [([1], [1], [1], [1], [2, 1], [0, 1, 0, 0])]
            }
        self.il._demote_monosyllable_stress()
        self.m.check_validity_and_continue.assert_called()
        self.m.check_validity_and_continue.assert_called_with([
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
        self.il._unique_dict_of_realized_stress_patterns = {
            (0, 1, 0, 0, 0, 0, 0, 0, 0, 0): [([0], [1], [0], [0], [0], [0], [0], [0], [0], [0])],

            }
        self.il._demote_monosyllable_stress()
        self.m.check_validity_and_continue.assert_called()
        self.m.check_validity_and_continue.assert_called_with([])    


    def test_promote_monosyllable_stresses(self):
        self.il._unique_dict_of_realized_stress_patterns = {
            (1, 0, 0, 0, 0, 2, 1, 0, 1, 0): [([1], [0, 1, 0, 0, 2], [1], [0], [1], [0])],

            }
        self.il._promote_monosyllable_stresses()
        self.m.check_validity_and_continue.assert_called()
        self.m.check_validity_and_continue.assert_called_with([
            ([1], [0, 1, 0, 0, 2], [1], [1], [1], [1]),
             ([1], [0, 1, 0, 0, 2], [1], [1], [1], [0]), 
             ([1], [0, 1, 0, 0, 2], [1], [0], [1], [1]), 
             ([1], [0, 1, 0, 0, 2], [1], [0], [1], [0])        
        ])   

    def test_promote_monosyllable_stresses_unchanged(self):
        self.il._unique_dict_of_realized_stress_patterns = {
            (1, 0, 0, 0, 0, 2, 1, 1, 1, 1): [([1], [0, 1, 0, 0, 2], [1], [1], [1], [1])],

            }
        self.il._promote_monosyllable_stresses()
        self.m.check_validity_and_continue.assert_called()
        self.m.check_validity_and_continue.assert_called_with([])   


    def test_promote_polysyllabic_zero_stresses(self):
        self.il._unique_dict_of_realized_stress_patterns = {
            (1, 0, 0, 0, 0, 2, 1, 1, 1, 1): [([1], [0, 1, 0, 0, 2], [1], [1], [1], [1])],

            }
        self.il._promote_polysyllabic_zero_stresses()
        self.m.check_validity_and_continue.assert_called()
        self.m.check_validity_and_continue.assert_called_with([
            ([1], [0, 1, 0, 0, 2], [1], [1], [1], [1]), 
            ([1], [0, 1, 2, 0, 2], [1], [1], [1], [1]), 
            ([1], [2, 1, 0, 0, 2], [1], [1], [1], [1]), 
            ([1], [2, 1, 2, 0, 2], [1], [1], [1], [1]), 
            ])  


    def test_promote_polysyllabic_zero_stresses_unchanged(self):
        self.il._unique_dict_of_realized_stress_patterns = {
            (1, 0, 0, 0, 0, 2, 1, 1, 1, 1): [([1], [1, 1, 2, 0, 2], [1], [1], [1], [1])],

            }
        self.il._promote_polysyllabic_zero_stresses()
        self.m.check_validity_and_continue.assert_called()
        self.m.check_validity_and_continue.assert_called_with([
            ([1], [1, 1, 2, 0, 2], [1], [1], [1], [1])
        ])  

    def test_demote_polysyllabic_primary_stresses(self):
        self.il._unique_dict_of_realized_stress_patterns = {
            (1, 0, 0, 0, 0, 2, 1, 1, 1, 1): [([1], [1, 1, 2, 0, 2], [1], [1], [1], [1])],

            }
        self.il._promote_polysyllabic_zero_stresses()
        self.m.check_validity_and_continue.assert_called()
        self.m.check_validity_and_continue.assert_called_with([
            ([1], [1, 1, 2, 0, 2], [1], [1], [1], [1])
        ])     


    def test_promote_polysyllabic_zero_stresses_multiple_lines(self):
        self.il._unique_dict_of_realized_stress_patterns = {
            (0, 0, 0, 1, 1, 1, 0, 1, 0, 0): [([0], [0], [0], [1], [1, 1], [0, 1, 0, 0])],
            (0, 0, 0, 1, 1, 2, 0, 1, 0, 0): [([0], [0], [0], [1], [1, 2], [0, 1, 0, 0])],
            (0, 0, 0, 1, 1, 1, 0, 1, 0, 0): [([0], [0], [0], [1], [1, 1], [0, 1, 0, 0])],
            }
        self.il._promote_polysyllabic_zero_stresses()
        self.m.check_validity_and_continue.assert_called()
        self.m.check_validity_and_continue.assert_called_with([
            ([0], [0], [0], [1], [1, 1], [0, 1, 0, 0]),
            ([0], [0], [0], [1], [1, 1], [0, 1, 0, 2]),
            ([0], [0], [0], [1], [1, 2], [0, 1, 0, 0]),
            ([0], [0], [0], [1], [1, 2], [0, 1, 0, 2])
        ])  


    def test_demote_polysyllabic_primary_stresses(self):
        self.il._unique_dict_of_realized_stress_patterns = {
            (1, 0, 0, 0, 0, 2, 1, 1, 1, 0): [([1], [1, 1, 2, 0, 2], [1], [1], [1, 2])],

            }
        self.il._demote_polysyllabic_primary_stresses()
        self.m.check_validity_and_continue.assert_called()
        self.m.check_validity_and_continue.assert_called_with([
            ([1], [1, 2, 2, 0, 2], [1], [1], [2, 2]), 
            ([1], [1, 2, 2, 0, 2], [1], [1], [1, 2]), 
            ([1], [1, 1, 2, 0, 2], [1], [1], [2, 2]), 
            ([1], [1, 1, 2, 0, 2], [1], [1], [1, 2])
        ])   


if __name__ == "__main__":
    unittest.main()