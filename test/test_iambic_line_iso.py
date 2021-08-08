import unittest
from unittest.mock import MagicMock
from iambic_line_processors.iambic_line import IambicLine




class TestIambicLineIso(unittest.TestCase):

    def setUp(self):
        self.il = IambicLine("", DEV=True)
        self.m = MagicMock()
        self.il.check_validity_and_continue = self.m.check_validity_and_continue


    def test_demote_compound_stress_unchanged(self):
        """
        Both deregulatory Heav'n their light,
        """
        self.il.unique_dict_of_realized_stress_patterns = {
            (1, 0, 1, 0, 0, 2, 0, 0, 1, 1): [([1], [0, 1, 0, 0, 2, 0], [0], [1], [1])],
            (1, 0, 1, 0, 0, 2, 0, 1, 1, 1): [([1], [0, 1, 0, 0, 2, 0], [1], [1], [1])]
            }
        self.il.demote_compound_stress()
        self.m.check_validity_and_continue.assert_called()
        self.m.check_validity_and_continue.assert_called_with(
            [([1], [0, 1, 0, 0, 2, 0], [0], [1], [1]), 
            ([1], [0, 1, 0, 0, 2, 0], [1], [1], [1])]
            )
    

    def test_demote_compound_stress(self):
        """
        Sees his own face, self-slain Humanity
        """
        self.il.unique_dict_of_realized_stress_patterns = {
            (1, 0, 1, 1, 1, 1, 0, 1, 0, 0): [([1], [0], [1], [1], [1, 1], [0, 1, 0, 0])],
            (1, 1, 1, 1, 1, 1, 0, 1, 0, 0): [([1], [1], [1], [1], [1, 1], [0, 1, 0, 0])]
            }
        self.il.demote_compound_stress()
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
        self.il.unique_dict_of_realized_stress_patterns = {
            (1, 0, 1, 1, 1, 1, 0, 1, 0, 0): [([1], [0], [1], [1], [1, 1], [0, 1, 0, 0])],
            (1, 0, 1, 1, 1, 2, 0, 1, 0, 0): [([1], [0], [1], [1], [1, 2], [0, 1, 0, 0])],
            (1, 0, 1, 1, 2, 1, 0, 1, 0, 0): [([1], [0], [1], [1], [2, 1], [0, 1, 0, 0])],
            (1, 1, 1, 1, 1, 1, 0, 1, 0, 0): [([1], [1], [1], [1], [1, 1], [0, 1, 0, 0])],
            (1, 1, 1, 1, 1, 2, 0, 1, 0, 0): [([1], [1], [1], [1], [1, 2], [0, 1, 0, 0])],
            (1, 1, 1, 1, 2, 1, 0, 1, 0, 0): [([1], [1], [1], [1], [2, 1], [0, 1, 0, 0])]
            }
        self.il.demote_monosyllable_stress()
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
        self.il.unique_dict_of_realized_stress_patterns = {
            (0, 1, 0, 0, 0, 0, 0, 0, 0, 0): [([0], [1], [0], [0], [0], [0], [0], [0], [0], [0])],

            }
        self.il.demote_monosyllable_stress()
        self.m.check_validity_and_continue.assert_called()
        self.m.check_validity_and_continue.assert_called_with([])    


    def test_promote_monosyllable_stresses(self):
        self.il.unique_dict_of_realized_stress_patterns = {
            (1, 0, 0, 0, 0, 2, 1, 0, 1, 0): [([1], [0, 1, 0, 0, 2], [1], [0], [1], [0])],

            }
        self.il.promote_monosyllable_stresses()
        self.m.check_validity_and_continue.assert_called()
        self.m.check_validity_and_continue.assert_called_with([
            ([1], [0, 1, 0, 0, 2], [1], [1], [1], [1]),
             ([1], [0, 1, 0, 0, 2], [1], [1], [1], [0]), 
             ([1], [0, 1, 0, 0, 2], [1], [0], [1], [1]), 
             ([1], [0, 1, 0, 0, 2], [1], [0], [1], [0])        
        ])   

    def test_promote_monosyllable_stresses_unchanged(self):
        self.il.unique_dict_of_realized_stress_patterns = {
            (1, 0, 0, 0, 0, 2, 1, 1, 1, 1): [([1], [0, 1, 0, 0, 2], [1], [1], [1], [1])],

            }
        self.il.promote_monosyllable_stresses()
        self.m.check_validity_and_continue.assert_called()
        self.m.check_validity_and_continue.assert_called_with([])   


    def test_promote_polysyllabic_zero_stresses(self):
        self.il.unique_dict_of_realized_stress_patterns = {
            (1, 0, 0, 0, 0, 2, 1, 1, 1, 1): [([1], [0, 1, 0, 0, 2], [1], [1], [1], [1])],

            }
        self.il.promote_polysyllabic_zero_stresses()
        self.m.check_validity_and_continue.assert_called()
        self.m.check_validity_and_continue.assert_called_with([
            ([1], [0, 1, 0, 0, 2], [1], [1], [1], [1]), 
            ([1], [0, 1, 2, 0, 2], [1], [1], [1], [1]), 
            ([1], [2, 1, 0, 0, 2], [1], [1], [1], [1]), 
            ([1], [2, 1, 2, 0, 2], [1], [1], [1], [1]), 
            ])  


    def test_promote_polysyllabic_zero_stresses_unchanged(self):
        self.il.unique_dict_of_realized_stress_patterns = {
            (1, 0, 0, 0, 0, 2, 1, 1, 1, 1): [([1], [1, 1, 2, 0, 2], [1], [1], [1], [1])],

            }
        self.il.promote_polysyllabic_zero_stresses()
        self.m.check_validity_and_continue.assert_called()
        self.m.check_validity_and_continue.assert_called_with([
            ([1], [1, 1, 2, 0, 2], [1], [1], [1], [1])
        ])  



if __name__ == "__main__":
    unittest.main()