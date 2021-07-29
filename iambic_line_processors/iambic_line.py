from itertools import product
from pprint import pprint



class IambicLine():
    """
    should ultimately modifiy self.tokens with the final stresses?
    Should try each rule at a time, then all of them combined?
    Maybe accumulate with each additional rule (keep an "all_possibilities" attribute and add to it for every rule application)
    """

    BASE_PATTERN = (0,1,0,1,0,1,0,1,0,1)
    # WORD_STRESS_PATTERNS = {
    #     2: ( [0,1], [1,0] ),
    #     3: ( ([0,0,1], [1,0,1]), ([0,1,0], [0,1,0]), ([1,0,0], [1,0,1]) ),
    #     4: ( ([0,0,0,1], [0,1,0,1]), ([0,0,1,0], [1,0,1,0]), ([0,1,0,0], [0,1,0,1]), ([1,0,0,0], [1,0,1,0]) ),
    #     5: ( [0,0,0,0,1], [0,0,0,1,0], [0,0,1,0,0], [0,1,0,0,0], [1,0,0,0,0] ),
    #     6: ( [0,0,0,0,0,1], [0,0,0,0,1,0], [0,0,0,1,0,0], [0,0,1,0,0,0], [0,1,0,0,0,0], [1,0,0,0,0,0] )
    # }
    WORD_STRESS_PATTERNS = {
        2: ( [0,1], [1,0] ),
        3: {
            (0,0,1): [1,0,1],
            (0,1,0): [0,1,0],
            (1,0,0): [1,0,1]
        },
        4: {
            (0,0,0,1): [0,1,0,1],
            (0,0,1,0): [1,0,1,0],
            (0,1,0,0): [0,1,0,1],
            (1,0,0,0): [1,0,1,0]
        },
        5: {
            (0,1,0,2,0): [0,1,0,1,0]
        }
    }

    def __init__(self, tokens):
        # self.tokens = tokens
        self.base_stresses = self.get_base_stress_patterns(tokens)
        self.valid_pattern = None
        self.unmodified_check_complete = False
        self.promote_secondary_check_complete = False
        self.alter_primary_check_complete = False
        self.demote_monosyllable_check_complete = False
        self.promote_polysyllabic_zero_check_complete = False

    def get_base_stress_patterns(self, tokens):
        """
        accepts: List of Tokens: [Token, Token, Token, Token, Token]
        returns: List of Tuples - [([[0], [1], [0]], 'the'), ([[2, 0, 1, 0]], 'expeditious'), ([[1]], 'pass'), ([[1, 2], [0, 1]], 'address'), ([[0, 1], [0, 1]], 'within')]
        """
        base_stresses = [(t.stress_patterns, t.token) for t in tokens]
        # print("*****", base_stresses)

        return base_stresses

    def get_possible_stress_variation_combinations(self, base_stresses):
        """
        accepts: List of Tuples - [([[0], [1], [0]], 'the'), ([[2, 0, 1, 0]], 'expeditious'), ([[1]], 'pass'), ([[1, 2], [0, 1]], 'address'), ([[0, 1], [0, 1]], 'within')]
        returns: List of Tuples (stress variation combinations) - [([0], [2, 0, 1, 0], [1], [1, 2], [0, 1]), ([0], [2, 0, 1, 0], [1], [1, 2], [0, 1]), ([0], [2, 0, 1, 0], [1], [0, 1], [0, 1]), ([0], [2, 0, 1, 0], [1], [0, 1], [0, 1]), ([1], [2, 0, 1, 0], [1], [1, 2], [0, 1]), ([1], [2, 0, 1, 0], [1], [1, 2], [0, 1]), ([1], [2, 0, 1, 0], [1], [0, 1], [0, 1]), ([1], [2, 0, 1, 0], [1], [0, 1], [0, 1]), ([0], [2, 0, 1, 0], [1], [1, 2], [0, 1]), ([0], [2, 0, 1, 0], [1], [1, 2], [0, 1]), ([0], [2, 0, 1, 0], [1], [0, 1], [0, 1]), ([0], [2, 0, 1, 0], [1], [0, 1], [0, 1])]
        """
        stress_variation_combinations = list(product(*[pair[0] for pair in base_stresses]))
        return stress_variation_combinations

    def get_actual_stress_possibilities(self, stress_variation_combinations):
        # print("get_actual_stress_possibilities called")
        # print("stress_variation_combinations: ", stress_variation_combinations)
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
        print("is_valid_IP", self.unmodified_check_complete, self.promote_secondary_check_complete, self.demote_monosyllable_check_complete,self.promote_polysyllabic_zero_check_complete, self.alter_primary_check_complete)
        if self.demote_monosyllable_check_complete:
            print("is_valid_IP, actual_stress_possibilities")
            pprint([ x["formatted"] for x in actual_stress_possibilities])

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

        self.unmodified_check_complete = True
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
            # print("MOD: ", mod)
            new_combinations.append(tuple(mod))

        stress_variation_combinations = new_combinations
        actual_stress_possibilities = self.get_actual_stress_possibilities(stress_variation_combinations)

        self.promote_secondary_check_complete = True
        return self.is_valid_IP(actual_stress_possibilities)


    def demote_monosyllable_stress(self):
        # print("demote_monosyllable_stress", self.unmodified_check_complete, self.promote_secondary_check_complete, self.alter_primary_check_complete, self.demote_monosyllable_check_complete)
        """
        simplified: any monosyllable can be demoted
        """
        # actual_stress_possibilities = self.initial_processing()
        combinations = self.get_possible_stress_variation_combinations(self.base_stresses)


        new_combinations = []
        i = 0
        for combination in combinations:
            mod = []
            for word in combination:
                mod.append([0 if s == 1 and len(word) == 1 and i % 2 == 0 else s for s in word])
                i = i + len(word)
            poss = tuple(mod)
            if poss in new_combinations:
                pass
            else:
                new_combinations.append(poss)
            i = 0

        zipped = list(zip(combinations, new_combinations))
        demoted_combinations = [[*pair] for pair in zipped]
        cartesian_product = list(product(*[combo for combo in demoted_combinations]))
        flattened_cartesian_product = [x for y in cartesian_product for x in y]
        stress_variation_combinations = flattened_cartesian_product
        actual_stress_possibilities = self.get_actual_stress_possibilities(stress_variation_combinations)
        self.demote_monosyllable_check_complete = True
        return self.is_valid_IP(actual_stress_possibilities)


    # helper
    def get_polysyllabic_stress_possibilities(self, word):
        try:
            multi_stressed = self.WORD_STRESS_PATTERNS[len(word)][tuple(word)]
            return multi_stressed
        except:
            print("*" * 80, "polysyllabic pattern not found:", word)


    def promote_polysyllabic_zero_stresses(self):
        """
        check if the word requires two stresses
        """
        print("promote_polysyllabic_zero_stresses")
        combinations = self.get_possible_stress_variation_combinations(self.base_stresses)

        new_combinations = []
        i = 0
        for combination in combinations:
            mod = []
            # print(combination)
            for word in combination:
                if len(word) == 3 and i % 2 == 1:
                    print("three letter word needs two syllables")
                    # print(word)
                elif len(word) > 3:
                    print("more than 3 syllable word, needs more than 1 stress")
                    multi_stressed = self.get_polysyllabic_stress_possibilities(word)
                    mod.append(multi_stressed)
                else:
                    mod.append(word)
                i = i + len(word)
            poss = tuple(mod)
            if poss in new_combinations:
                pass
            else:
                new_combinations.append(poss)
            i = 0
            # new_combinations.append(mod)
        # print("new_combinations: ", new_combinations)

        zipped = list(zip(combinations, new_combinations))
        promoted_combinations = [[*pair] for pair in zipped]
        cartesian_product = list(product(*[combo for combo in promoted_combinations]))
        flattened_cartesian_product = [x for y in cartesian_product for x in y]
        stress_variation_combinations = flattened_cartesian_product
        actual_stress_possibilities = self.get_actual_stress_possibilities(stress_variation_combinations)
        print("polysyllabic actual_stress_possibilities: ", len(actual_stress_possibilities))
        self.promote_polysyllabic_zero_check_complete = True
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
        self.alter_primary_check_complete = True
        return self.is_valid_IP(actual_stress_possibilities)   



    def fit_to_IP(self):
        if self.alter_primary_check_complete: 
            return False
        if self.unmodified_check_complete and not self.promote_secondary_check_complete:
            return self.promote_secondary_stresses()
        if self.unmodified_check_complete and self.promote_secondary_check_complete:
            if not self.demote_monosyllable_check_complete:
                return self.demote_monosyllable_stress()
            if not self.promote_polysyllabic_zero_check_complete:
                return self.promote_polysyllabic_zero_stresses()
            if self.alter_primary_stresses():
                return True
        return False



