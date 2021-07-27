from itertools import product
from pprint import pprint



class IambicLine():
    """
    should ultimately modifiy self.tokens with the final stresses?
    """

    BASE_PATTERN = (0,1,0,1,0,1,0,1,0,1)
    WORD_STRESS_PATTERNS = {
        2: ( [0,1], [1,0] ),
        3: ( [0,0,1], [0,1,0], [1,0,0] ),
        4: ( [0,0,0,1], [0,0,1,0], [0,1,0,0], [1,0,0,0] ),
        5: ( [0,0,0,0,1], [0,0,0,1,0], [0,0,1,0,0], [0,1,0,0,0], [1,0,0,0,0] ),
        6: ( [0,0,0,0,0,1], [0,0,0,0,1,0], [0,0,0,1,0,0], [0,0,1,0,0,0], [0,1,0,0,0,0], [1,0,0,0,0,0] )
    }

    def __init__(self, tokens):
        # self.tokens = tokens
        self.base_stresses = self.get_base_stress_patterns(tokens)
        self.valid_pattern = None
        self.round_1_complete = False
        self.round_2_complete = False
        self.round_3_complete = False

    def get_base_stress_patterns(self, tokens):
        """
        accepts: List of Tokens: [Token, Token, Token, Token, Token]
        returns: List of Tuples - [([[0], [1], [0]], 'the'), ([[2, 0, 1, 0]], 'expeditious'), ([[1]], 'pass'), ([[1, 2], [0, 1]], 'address'), ([[0, 1], [0, 1]], 'within')]
        """
        base_stresses = [(t.stress_patterns, t.token) for t in tokens]
        return base_stresses

    def get_possible_stress_variation_combinations(self, base_stresses):
        """
        accepts: List of Tuples - [([[0], [1], [0]], 'the'), ([[2, 0, 1, 0]], 'expeditious'), ([[1]], 'pass'), ([[1, 2], [0, 1]], 'address'), ([[0, 1], [0, 1]], 'within')]
        returns: List of Tuples (stress variation combinations) - [([0], [2, 0, 1, 0], [1], [1, 2], [0, 1]), ([0], [2, 0, 1, 0], [1], [1, 2], [0, 1]), ([0], [2, 0, 1, 0], [1], [0, 1], [0, 1]), ([0], [2, 0, 1, 0], [1], [0, 1], [0, 1]), ([1], [2, 0, 1, 0], [1], [1, 2], [0, 1]), ([1], [2, 0, 1, 0], [1], [1, 2], [0, 1]), ([1], [2, 0, 1, 0], [1], [0, 1], [0, 1]), ([1], [2, 0, 1, 0], [1], [0, 1], [0, 1]), ([0], [2, 0, 1, 0], [1], [1, 2], [0, 1]), ([0], [2, 0, 1, 0], [1], [1, 2], [0, 1]), ([0], [2, 0, 1, 0], [1], [0, 1], [0, 1]), ([0], [2, 0, 1, 0], [1], [0, 1], [0, 1])]
        """
        stress_variation_combinations = list(product(*[pair[0] for pair in base_stresses]))
        return stress_variation_combinations

    def get_actual_stress_possibilities(self, stress_variation_combinations):
        """
        accepts: List of Tuples (stress variation combinations) - [([0], [2, 0, 1, 0], [1], [1, 2], [0, 1]), ([0], [2, 0, 1, 0], [1], [1, 2], [0, 1]), ([0], [2, 0, 1, 0], [1], [0, 1], [0, 1]), ([0], [2, 0, 1, 0], [1], [0, 1], [0, 1]), ([1], [2, 0, 1, 0], [1], [1, 2], [0, 1]), ([1], [2, 0, 1, 0], [1], [1, 2], [0, 1]), ([1], [2, 0, 1, 0], [1], [0, 1], [0, 1]), ([1], [2, 0, 1, 0], [1], [0, 1], [0, 1]), ([0], [2, 0, 1, 0], [1], [1, 2], [0, 1]), ([0], [2, 0, 1, 0], [1], [1, 2], [0, 1]), ([0], [2, 0, 1, 0], [1], [0, 1], [0, 1]), ([0], [2, 0, 1, 0], [1], [0, 1], [0, 1])]
        returns: List of Dictionaries - [{'formatted': (0, 2, 0, 1, 0, 1, 1, 2, 0, 1), 'original': ([0], [2, 0, 1, 0], [1], [1, 2], [0, 1])}, {'formatted': (0, 2, 0, 1, 0, 1, 1, 2, 0, 1), 'original': ([0], [2, 0, 1, 0], [1], [1, 2], [0, 1])}, {'formatted': (0, 2, 0, 1, 0, 1, 0, 1, 0, 1), 'original': ([0], [2, 0, 1, 0], [1], [0, 1], [0, 1])}, {'formatted': (0, 2, 0, 1, 0, 1, 0, 1, 0, 1), 'original': ([0], [2, 0, 1, 0], [1], [0, 1], [0, 1])}, {'formatted': (1, 2, 0, 1, 0, 1, 1, 2, 0, 1), 'original': ([1], [2, 0, 1, 0], [1], [1, 2], [0, 1])}, {'formatted': (1, 2, 0, 1, 0, 1, 1, 2, 0, 1), 'original': ([1], [2, 0, 1, 0], [1], [1, 2], [0, 1])}, {'formatted': (1, 2, 0, 1, 0, 1, 0, 1, 0, 1), 'original': ([1], [2, 0, 1, 0], [1], [0, 1], [0, 1])}, {'formatted': (1, 2, 0, 1, 0, 1, 0, 1, 0, 1), 'original': ([1], [2, 0, 1, 0], [1], [0, 1], [0, 1])}, {'formatted': (0, 2, 0, 1, 0, 1, 1, 2, 0, 1), 'original': ([0], [2, 0, 1, 0], [1], [1, 2], [0, 1])}, {'formatted': (0, 2, 0, 1, 0, 1, 1, 2, 0, 1), 'original': ([0], [2, 0, 1, 0], [1], [1, 2], [0, 1])}, {'formatted': (0, 2, 0, 1, 0, 1, 0, 1, 0, 1), 'original': ([0], [2, 0, 1, 0], [1], [0, 1], [0, 1])}, {'formatted': (0, 2, 0, 1, 0, 1, 0, 1, 0, 1), 'original': ([0], [2, 0, 1, 0], [1], [0, 1], [0, 1])}]
        """
        combos_list = []
        for c in stress_variation_combinations:
            f = tuple( s for w in c for s in w)
            line = {
                "formatted": f,
                "original": c
            }
            combos_list.append(line)
        return combos_list

    
    def initial_processing(self, stress_pattern_combinations=None):
        """
        accepts: List of Tuples - [([0], [2, 0, 1, 0], [1], [1, 2], [0, 1]), ([0], [2, 0, 1, 0], [1], [1, 2], [0, 1]), ([0], [2, 0, 1, 0], [1], [0, 1], [0, 1]), ([0], [2, 0, 1, 0], [1], [0, 1], [0, 1]), ([1], [2, 0, 1, 0], [1], [1, 2], [0, 1]), ([1], [2, 0, 1, 0], [1], [1, 2], [0, 1]), ([1], [2, 0, 1, 0], [1], [0, 1], [0, 1]), ([1], [2, 0, 1, 0], [1], [0, 1], [0, 1]), ([0], [2, 0, 1, 0], [1], [1, 2], [0, 1]), ([0], [2, 0, 1, 0], [1], [1, 2], [0, 1]), ([0], [2, 0, 1, 0], [1], [0, 1], [0, 1]), ([0], [2, 0, 1, 0], [1], [0, 1], [0, 1])]
        returns:  List of Dictionaries - [{'formatted': (0, 2, 0, 1, 0, 1, 1, 2, 0, 1), 'original': ([0], [2, 0, 1, 0], [1], [1, 2], [0, 1])}, {'formatted': (0, 2, 0, 1, 0, 1, 1, 2, 0, 1), 'original': ([0], [2, 0, 1, 0], [1], [1, 2], [0, 1])}, {'formatted': (0, 2, 0, 1, 0, 1, 0, 1, 0, 1), 'original': ([0], [2, 0, 1, 0], [1], [0, 1], [0, 1])}, {'formatted': (0, 2, 0, 1, 0, 1, 0, 1, 0, 1), 'original': ([0], [2, 0, 1, 0], [1], [0, 1], [0, 1])}, {'formatted': (1, 2, 0, 1, 0, 1, 1, 2, 0, 1), 'original': ([1], [2, 0, 1, 0], [1], [1, 2], [0, 1])}, {'formatted': (1, 2, 0, 1, 0, 1, 1, 2, 0, 1), 'original': ([1], [2, 0, 1, 0], [1], [1, 2], [0, 1])}, {'formatted': (1, 2, 0, 1, 0, 1, 0, 1, 0, 1), 'original': ([1], [2, 0, 1, 0], [1], [0, 1], [0, 1])}, {'formatted': (1, 2, 0, 1, 0, 1, 0, 1, 0, 1), 'original': ([1], [2, 0, 1, 0], [1], [0, 1], [0, 1])}, {'formatted': (0, 2, 0, 1, 0, 1, 1, 2, 0, 1), 'original': ([0], [2, 0, 1, 0], [1], [1, 2], [0, 1])}, {'formatted': (0, 2, 0, 1, 0, 1, 1, 2, 0, 1), 'original': ([0], [2, 0, 1, 0], [1], [1, 2], [0, 1])}, {'formatted': (0, 2, 0, 1, 0, 1, 0, 1, 0, 1), 'original': ([0], [2, 0, 1, 0], [1], [0, 1], [0, 1])}, {'formatted': (0, 2, 0, 1, 0, 1, 0, 1, 0, 1), 'original': ([0], [2, 0, 1, 0], [1], [0, 1], [0, 1])}]
        """
        stress_variation_combinations = stress_pattern_combinations if stress_pattern_combinations else self.get_possible_stress_variation_combinations(self.base_stresses)
        actual_stress_possibilities = self.get_actual_stress_possibilities(stress_variation_combinations)
        return actual_stress_possibilities


    def is_valid_IP(self, actual_stress_possibilities):
        print("is_valid_IP", self.round_1_complete, self.round_2_complete, self.round_3_complete)
        """
        accepts: List of Dictionaries - [{'formatted': (0, 2, 0, 1, 0, 1, 1, 2, 0, 1), 'original': ([0], [2, 0, 1, 0], [1], [1, 2], [0, 1])}, {'formatted': (0, 2, 0, 1, 0, 1, 1, 2, 0, 1), 'original': ([0], [2, 0, 1, 0], [1], [1, 2], [0, 1])}, {'formatted': (0, 2, 0, 1, 0, 1, 0, 1, 0, 1), 'original': ([0], [2, 0, 1, 0], [1], [0, 1], [0, 1])}, {'formatted': (0, 2, 0, 1, 0, 1, 0, 1, 0, 1), 'original': ([0], [2, 0, 1, 0], [1], [0, 1], [0, 1])}, {'formatted': (1, 2, 0, 1, 0, 1, 1, 2, 0, 1), 'original': ([1], [2, 0, 1, 0], [1], [1, 2], [0, 1])}, {'formatted': (1, 2, 0, 1, 0, 1, 1, 2, 0, 1), 'original': ([1], [2, 0, 1, 0], [1], [1, 2], [0, 1])}, {'formatted': (1, 2, 0, 1, 0, 1, 0, 1, 0, 1), 'original': ([1], [2, 0, 1, 0], [1], [0, 1], [0, 1])}, {'formatted': (1, 2, 0, 1, 0, 1, 0, 1, 0, 1), 'original': ([1], [2, 0, 1, 0], [1], [0, 1], [0, 1])}, {'formatted': (0, 2, 0, 1, 0, 1, 1, 2, 0, 1), 'original': ([0], [2, 0, 1, 0], [1], [1, 2], [0, 1])}, {'formatted': (0, 2, 0, 1, 0, 1, 1, 2, 0, 1), 'original': ([0], [2, 0, 1, 0], [1], [1, 2], [0, 1])}, {'formatted': (0, 2, 0, 1, 0, 1, 0, 1, 0, 1), 'original': ([0], [2, 0, 1, 0], [1], [0, 1], [0, 1])}, {'formatted': (0, 2, 0, 1, 0, 1, 0, 1, 0, 1), 'original': ([0], [2, 0, 1, 0], [1], [0, 1], [0, 1])}]
        returns: Boolean
        """
        for s in actual_stress_possibilities:
            normal = tuple(syl for syl in s["formatted"])
            if normal == self.BASE_PATTERN:
                self.valid_pattern = s
                # self.get_closest_fit()
                return True

        self.round_1_complete = True
        return self.fit_to_IP()
 


    def promote_secondary_stresses(self):
        """
        accepts:
        returns:
        """
        actual_stress_possibilities = self.initial_processing()

        combinations = self.get_possible_stress_variation_combinations(self.base_stresses)
        new_combinations = []
        for combination in combinations:
            mod = []
            for word in combination:
                mod.append([1 if s == 2 and len(word) > 2 else s for s in word])
            new_combinations.append(tuple(mod))

        stress_variation_combinations = new_combinations
        actual_stress_possibilities = self.get_actual_stress_possibilities(stress_variation_combinations)

        self.round_2_complete = True
        return self.is_valid_IP(actual_stress_possibilities)



    def alter_primary_stresses(self):
        possibles = self.get_possible_stress_variation_combinations(self.base_stresses)
        new_possibles = []
        for c in possibles:
            for i,w in enumerate(c):
                if len(w) > 1:
                    for variant in self.WORD_STRESS_PATTERNS[len(w)]:
                        c_copy = [w for w in c]
                        c_copy[i] = variant
                        new_possibles.append(tuple(c_copy))
        actual_stress_possibilities = self.initial_processing(new_possibles)
        self.round_3_complete = True
        return self.is_valid_IP(actual_stress_possibilities)   



    def fit_to_IP(self):
        if self.round_3_complete: 
            return False
        if self.round_1_complete and not self.round_2_complete:
            return self.promote_secondary_stresses()
        if self.round_1_complete and self.round_2_complete:
            if self.alter_primary_stresses():
                return True
        return False
