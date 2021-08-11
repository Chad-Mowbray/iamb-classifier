from itertools import product
from pprint import pprint
from iambic_line_processors.combinations_graph import CombinationsGraph



class IambicLine():

    #TODO: to manage state, create an object {0: unmodified, 1: promote_secondary...}
    #       and increment a counter for every is_valid_IP check, instead of current switches

    BASE_PATTERN = (0,1,0,1,0,1,0,1,0,1)

    def __init__(self, tokens, DEV=False):
        self.tokens = tokens
        self.original_stress_patterns_per_token = []
        self.formatted_list_of_realized_stress_patterns = []
        self.unique_dict_of_realized_stress_patterns = {}
        self.is_valid_pattern = False
        self.valid_pattern = None
        self.current_state = 0
        self.rules_applied = []
        self.syllables_per_line = []
        self.altered_patterns = []
        self.changed_words = []

        if not DEV: self.main()

    def __str__(self):
        return f"{self.is_valid_pattern}, {len(self.rules_applied)}, {self.syllables_per_line}, {self.altered_patterns}, {self.changed_words}"

    
    def get_transformed_words(self, comparisons):
        # TODO 
        """
        This is still very approximate
        """
        print("get_transformed_words called")
        # pprint(comparisons)
        for comparison in comparisons:
            abstract,detailed = comparison
            # print(abstract, detailed)
            detailed = [x for y in detailed for x in y]
            # print(detailed)
            original = [x for x in [x for y in self.original_stress_patterns_per_token for x in y] if type(x) == list]
            # print("O:",original, "D", detailed)
            for i,word_group in enumerate(original):
                if detailed[i] in word_group or len(detailed[i]) < 2 or self.current_state <= 5:
                    continue
                    # print("match")
                else:
                    print('novel')
                    print('\t', detailed[i], word_group)
                    changed_word = self.original_stress_patterns_per_token[i][1]
                    print("changed word", changed_word)
                    self.changed_words.append(changed_word)
                    self.altered_patterns.append(detailed[i])


    def test_base_pattern(self):
        comparisons = []
        for potential,original in self.unique_dict_of_realized_stress_patterns.items():
            if len(potential) != len(self.BASE_PATTERN): continue
            # comparison = [syl for i,syl in enumerate(potential) if i % 2 == 0 and syl in [0,2] or i % 2 == 1 and syl == self.BASE_PATTERN[i] ]
            comparison = [syl for i,syl in enumerate(potential) if i % 2 == 0 and syl in [0,2] or i % 2 == 1 and syl in [1,2] ] # Should secondary work for either position?

            if len(comparison) == len(self.BASE_PATTERN):
                # print("comparison: ", comparison)
                # print("formatted_list_of_realized_stress_patterns:")
                # pprint(self.formatted_list_of_realized_stress_patterns)
                comparisons.append([comparison, original])
        if comparisons: 
            # print("))))))))))))")
            self.get_transformed_words(comparisons)
            # print(self.original_stress_patterns_per_token)
            # pprint(comparisons)
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
        # pprint(self.unique_dict_of_realized_stress_patterns)


    def get_syllables_per_line(self):
        print("from get_syllables_per_line: ")
        # pprint(self.unique_dict_of_realized_stress_patterns)
        for pattern in self.unique_dict_of_realized_stress_patterns:
            if len(pattern) not in self.syllables_per_line:
                self.syllables_per_line.append(len(pattern))


    def is_valid_IP(self):
        self.get_syllables_per_line()
        if self.test_base_pattern():
            print("##"*60, self.current_state)
            return True
        else:
            # print("INVALID"*80)
            return self.fit_to_IP()


    def fit_to_IP(self):
        """
        After the initial check:
            1. Demote compound-word stresses
            2. Demote monosyllable stresses
            3. Promote monosyllable stresses
            4. Promote polysyllabic zero stresses 
            5. Demote polysyllabic zero stresses
        """

        phases = {
            1: self.demote_compound_stress,
            2: self.demote_monosyllable_stress,
            3: self.promote_monosyllable_stresses,
            4: self.promote_polysyllabic_zero_stresses, #TODO but only to 2?
            5: self.demote_polysyllabic_primary_stresses,
            # 6: self.alter_primary_stresses # demote polysyllable stress
        }
        self.rules_applied.append(phases[self.current_state].__name__)
        try:
            if phases[self.current_state]():
                return True
            else:
                return False
        except KeyError:
            print("Ran out of transformations")
            self.current_state += 1
            self.rules_applied.append("FAILURE")
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


    def promote_polysyllabic_zero_stresses(self):
        #TODO: bisyllabic words should get promoted first, this should promote to 2
        """
        check if the word requires more than one stress
        can promote appropriate 0s to 2s
        """
        print('promote_polysyllabic_zero_stresses called')
        new_combinations = []
        for line in self.get_baseline_before_alteration():
            cg = CombinationsGraph([line], [0,2], True, 0)
            single_combinations = cg.new_combinations
            for single_combination in single_combinations:
                new_combinations.append(single_combination)

        return self.check_validity_and_continue(new_combinations)


    def demote_polysyllabic_primary_stresses(self):
        print("demote_polysyllabic_primary_stresses called")
        print(self.tokens)
        new_combinations = []
        for line in self.get_baseline_before_alteration():
            cg = CombinationsGraph([line], [2, 1], False, 1)
            single_combinations = cg.new_combinations
            for single_combination in single_combinations:
                new_combinations.append(single_combination)

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
        print("main called")
        self.tokens = [t for t in self.tokens if t.token != "th'"]  # remove elided "the"
        self.original_stress_patterns_per_token = self.get_original_stress_patterns_per_token()
        print("original stress patterns per token: ", self.original_stress_patterns_per_token)
        possible_stress_patterns_per_token = self.get_possible_stress_patterns_per_token(self.original_stress_patterns_per_token)
        print("LLLLLLLLLLLLL: ", possible_stress_patterns_per_token)
        self.is_valid_pattern = self.check_validity_and_continue(possible_stress_patterns_per_token)
        # print(self.is_valid_pattern)
        
