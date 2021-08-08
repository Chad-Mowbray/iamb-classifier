from itertools import product
from pprint import pprint
from iambic_line_processors.combinations_graph import CombinationsGraph




class IambicLine():

    #TODO: to manage state, create an object {0: unmodified, 1: promote_secondary...}
    #       and increment a counter for every is_valid_IP check, instead of current switches

    BASE_PATTERN = (0,1,0,1,0,1,0,1,0,1)
    WORD_STRESS_PATTERNS = {
        2: ( [0,1], [1,0] ),
        3: ( [0,1,0], [1,0,1] ),
        4: ( [0,1,0,1], [1,0,1,0] ),
        5: ( [0,1,0,1,0], [1,0,1,0,1] ),
        6: ( [0,1,0,1,0,1], [1,0,1,0,1,0] ),
        7: ( [0,1,0,1,0,1,0], [1,0,1,0,1,0,1] )
    }


    def __init__(self, tokens, DEV=False):
        self.tokens = tokens
        self.formatted_list_of_realized_stress_patterns = []
        self.unique_dict_of_realized_stress_patterns = {}
        self.is_valid_pattern = False
        self.valid_pattern = None
        self.current_state = 0
        self.rules_applied = []
        self.syllables_per_line = []
        self.altered_pattern = []

        if not DEV: self.main()

    def __str__(self):
        return f"{self.is_valid_pattern}, {len(self.rules_applied)}, {self.syllables_per_line}, {self.altered_pattern}"


    def test_base_pattern(self):
        for potential in self.unique_dict_of_realized_stress_patterns:
            if len(potential) != len(self.BASE_PATTERN): continue
            # comparison = [syl for i,syl in enumerate(potential) if i % 2 == 0 and syl in [0,2] or i % 2 == 1 and syl == self.BASE_PATTERN[i] ]
            comparison = [syl for i,syl in enumerate(potential) if i % 2 == 0 and syl in [0,2] or i % 2 == 1 and syl in [1,2] ] # Should secondary work for either position?

            if len(comparison) == len(self.BASE_PATTERN):
                return True
        return False


    def get_original_stress_patterns_per_token(self):
        return [(t.stress_patterns, t.token) for t in self.tokens]


    def get_possible_stress_patterns_per_token(self, original_stress_patterns_per_token):
        """
        returns: List[Tuples(Lists)]
        """
        return list(product(*[pair[0] for pair in original_stress_patterns_per_token]))


    def create_formatted_list_of_realized_stress_patterns(self, stress_patterns_per_token):
        """
        accepts: List[Tuples(Lists)]
        produces: 
            -adds on to self.formatted_list_of_realized_stress_patterns -- List[Dictionaries]
            -adds unique values to unique_dict_of_realized_stress_patterns -- Dict{Tuple: List[Tuples(Lists)]}
        """
        formatted_list_of_realized_stress_patterns = []
        for pattern in stress_patterns_per_token:
            f = tuple( syllable for word in pattern for syllable in word)
            line = {
                "formatted": f,
                "original": pattern
            }
            formatted_list_of_realized_stress_patterns.append(line) 
        self.formatted_list_of_realized_stress_patterns.extend(formatted_list_of_realized_stress_patterns)
        self.create_unique_dict_of_realized_stress_patterns()


    def create_unique_dict_of_realized_stress_patterns(self):
        for entry in self.formatted_list_of_realized_stress_patterns:
            if self.unique_dict_of_realized_stress_patterns.get(entry["formatted"]):
                if entry["original"] not in self.unique_dict_of_realized_stress_patterns[entry["formatted"]]:
                    self.unique_dict_of_realized_stress_patterns[entry["formatted"]].append(entry["original"])
            else:
                self.unique_dict_of_realized_stress_patterns[entry["formatted"]] = [entry["original"]]
        print("initial unique_dict: ")
        pprint(self.unique_dict_of_realized_stress_patterns)



    def get_syllables_per_line(self):
        print("from get_syllables_per_line: ")
        pprint(self.unique_dict_of_realized_stress_patterns)
        for pattern in self.unique_dict_of_realized_stress_patterns:
            if len(pattern) not in self.syllables_per_line:
                self.syllables_per_line.append(len(pattern))


    def is_valid_IP(self):
        self.get_syllables_per_line()
        if self.test_base_pattern():
            print("##"*80)
            if self.current_state == 6: 
                self.altered_pattern = self.unique_dict_of_realized_stress_patterns[self.BASE_PATTERN]
            return True
        else:
            # print("INVALID"*80)
            return self.fit_to_IP()
        # if self.BASE_PATTERN in self.unique_dict_of_realized_stress_patterns:
            # if self.current_state == 6: 
            #     self.altered_pattern = self.unique_dict_of_realized_stress_patterns[self.BASE_PATTERN]
        #     return True
        # else:
        #     return self.fit_to_IP()


    def fit_to_IP(self):
        """
        After the initial check:
            1. Promote secondary Stresses
            2. Demote compound stresses
            3. Demote monosyllabic stresses
            4. Promote polysyllabic zero stresses
        """
        # phases = {
        #     1: self.promote_secondary_stresses,
        #     2: self.demote_compound_stress,
        #     3: self.demote_monosyllable_stress,
        #     4: self.promote_polysyllabic_zero_stresses, #TODO but only to 2?
        #     5: self.alter_primary_stresses
        # }
        phases = {
            1: self.demote_compound_stress,
            2: self.demote_monosyllable_stress,
            3: self.promote_monosyllable_stresses,
            # TODO: promote_monosyllable_stress
            4: self.promote_polysyllabic_zero_stresses, #TODO but only to 2?
            5: self.promote_secondary_stresses,
            # 6: self.alter_primary_stresses
        }
        self.rules_applied.append(phases[self.current_state].__name__)
        try:
            if phases[self.current_state]():
                return True
            else:
                return False
        except KeyError:
            print("Ran out of transformations")
            return False


    def promote_monosyllable_stresses(self):
        print("promote_monosyllable_stresses")
        new_combinations = []
        monosyllable_nonprimary_count = 0
        line_i = 0
        for line in self.get_baseline_before_alteration():
            monosyllable_nonprimary_idxs = []
            for i, word in enumerate(line):
                if len(word) == 1 and word[0] in [0,2] and line_i % 2 == 1:
                    monosyllable_nonprimary_count += 1
                    monosyllable_nonprimary_idxs.append(i)
                line_i += len(word)
            line_i = 0
            if monosyllable_nonprimary_idxs:
                for possible in product([1,0],repeat=len(monosyllable_nonprimary_idxs)):
                    line_copy = [w for w in line]
                    for i,val in enumerate(possible):
                        line_copy[monosyllable_nonprimary_idxs[i]] = [val]
                    new_combinations.append(tuple(line_copy))
        # print("promote monosyllables: ", new_combinations)
        return self.check_validity_and_continue(new_combinations)


    def promote_secondary_stresses(self):
        #TODO: should this run at the end? 
        """
        Works on a List[Tuples(Lists)]
        Creates a new List[Tuples(Lists)]
        """
        print('promote_secondary_stress called')
        new_combinations = [] # List[Tuples(Lists)]
        
        for line in self.get_baseline_before_alteration():
            # print(line)
            reconstituted_line = []
            for i,word in enumerate(line):
                try:
                    primary_idx = word.index(1)
                except ValueError:
                    primary_idx = 0
                secondary_idxs = [i for i,syl in enumerate(word) if syl == 2]
                if len(secondary_idxs) < 2: 
                    reconstituted_line.append(word)
                    continue
                multiples = []
                for secondary_idx in secondary_idxs:
                    word_copy = [s for s in word]
                    word_copy[secondary_idx], word_copy[primary_idx] = word_copy[primary_idx], word_copy[secondary_idx]
                    multiples.append(word_copy)
                reconstituted_line.append(multiples)
            print("@@@@@@ ", reconstituted_line)

                #TODO: create a new line for each new word


                # reconstituted_line.append([1 if s == 2 and len(word) > 2 else s for s in word]) # should prevent [1,1]?
                # reconstituted_line.append([1 if s == 2 else s for s in w])
            new_combinations.append(tuple(reconstituted_line))
        print()
        print(new_combinations)
        print()

        return self.check_validity_and_continue(new_combinations)

    @staticmethod
    def create_demoted_compound_variations(word):
        word_stress_variations = []
        for i,syllable in enumerate(word):
            if syllable == 1:
                word_copy = [*word]
                word_copy[i] = 2 # should be 2?
                word_stress_variations.append(word_copy)
                continue
        return word_stress_variations


    def demote_compound_stress(self):
        print('demote_compound_stress called')
        new_combinations = []
        primary_count = 0
        for line in self.get_baseline_before_alteration():
            for word in line:
                for syllable in word:
                    if syllable == 1:
                        primary_count += 1
                    if primary_count > 1:
                        word_stress_variations = self.create_demoted_compound_variations(word)
                        idx_word_in_line = line.index(word)
                        for word_stress_variation in word_stress_variations:
                            line_copy = [w for w in line]
                            line_copy[idx_word_in_line] = word_stress_variation
                            line_copy = tuple(line_copy)
                            new_combinations.append(line_copy)
                primary_count = 0
            new_combinations.append(line)
        print("&& ", new_combinations)
        return self.check_validity_and_continue(new_combinations)


    def demote_monosyllable_stress(self):
        print('demote_monosyllable_stress called')
        """
        Works on a List[Tuples(Lists)]
        Creates a new List[Tuples(Lists)]

        Only demotes possibles in weak position
        """
        new_combinations = []
        monosyllable_primary_count = 0
        line_i = 0
        for line in self.get_baseline_before_alteration():
            monosyllable_primary_idxs = []
            for i, word in enumerate(line):
                if len(word) == 1 and word[0] == 1 and line_i % 2 == 0:
                    monosyllable_primary_count += 1
                    monosyllable_primary_idxs.append(i)
                line_i += len(word)
            line_i = 0
            if monosyllable_primary_idxs:
                for possible in product([1,0],repeat=len(monosyllable_primary_idxs)):
                    line_copy = [w for w in line]
                    for i,val in enumerate(possible):
                        line_copy[monosyllable_primary_idxs[i]] = [val]
                    new_combinations.append(tuple(line_copy))
        # print("demote monosyllables: ", new_combinations)
        return self.check_validity_and_continue(new_combinations)


    #helper
    def get_polysyllabic_stress_possibilities(self, word):
        print('get_polysyllabic_stress_possibilities called with: ', word)

        new_polysyllabic_stresses = []
        primary_index = word.index(1)
        if primary_index == 0:
            new_polysyllabic_stresses.append(1)
        elif primary_index % 2 == 0:
            new_polysyllabic_stresses.append(2)
        else:
            new_polysyllabic_stresses.append(0)

        # TODO should return list of lists with all possible combinations
        for i in range(1,len(word)):
            if new_polysyllabic_stresses[i - 1] == 0 and word[i] == 0:
                new_polysyllabic_stresses.append(2)
            else:
                new_polysyllabic_stresses.append(word[i])
            # else:
            #     new_polysyllabic_stresses.append(0)
            # print(new_polysyllabic_stresses)

        return new_polysyllabic_stresses


    def promote_polysyllabic_zero_stresses(self):
        #TODO: bisyllabic words should get promoted first, this should promote to 2
        """
        check if the word requires more than one stress
        can promote appropriate 0s to 2s
        """
        print('promote_polysyllabic_zero_stresses called')
        cg = CombinationsGraph(self.get_baseline_before_alteration())
        new_combinations = cg.new_combinations
        # new_combinations = []
        # i = 0
        # for line in self.get_baseline_before_alteration():
        #     reconstituted_line = []
        #     for word in line:
                
        #         # if len(word) == 3 and i % 2 == 1:
        #         #     pass
        #         #     print("three letter word needs two syllables")
        #         #     print(word)
        #         if len(word) >= 3:
        #             # print(word, line)
        #             multi_stressed = self.get_polysyllabic_stress_possibilities(word) # TODO what about multiple variations?
        #             # print("multi_stressed", multi_stressed)
        #             reconstituted_line.append(multi_stressed)
        #         else:
        #             reconstituted_line.append(word)
        #         i = i + len(word)
        #     new_combinations.append(tuple(reconstituted_line))
        #     i = 0

        return self.check_validity_and_continue(new_combinations)


    def alter_primary_stresses(self):
        print("alter_primary_stresses called")
        new_combinations = []
        for line in self.get_baseline_before_alteration():
            for i,word in enumerate(line):
                print(word)
                if len(word) > 1:
                    for variant in self.WORD_STRESS_PATTERNS[len(word)]:
                        line_copy = [*line]
                        line_copy[i] = variant
                        new_combinations.append(tuple(line_copy))

        return self.check_validity_and_continue(new_combinations)


    def get_baseline_before_alteration(self):
        return (l for line in self.unique_dict_of_realized_stress_patterns.values() for l in line)

    def check_validity_and_continue(self, new_combinations):
        self.create_formatted_list_of_realized_stress_patterns(new_combinations)
        self.current_state += 1
        # pprint(self.unique_dict_of_realized_stress_patterns)
        self.is_valid_pattern = self.is_valid_IP()
        return self.is_valid_pattern


    def main(self):
        original_stress_patterns_per_token = self.get_original_stress_patterns_per_token()
        print("original stress patterns per token: ", original_stress_patterns_per_token)
        possible_stress_patterns_per_token = self.get_possible_stress_patterns_per_token(original_stress_patterns_per_token)
        print("LLLLLLLLLLLLL: ", possible_stress_patterns_per_token)
        self.is_valid_pattrn = self.check_validity_and_continue(possible_stress_patterns_per_token)
        # print(self.is_valid_pattern)
        
