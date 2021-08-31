from itertools import product
from .combinations_graph import CombinationsGraph



class IambicLine():
    """
    Takes a tokenized line of IP
    Checks if the line is a possible line of valid IP using the following process:
            0. No changes
            1. Demote compound-word stresses
            2. Demote monosyllable stresses
            3. Promote monosyllable stresses
            4. Promote polysyllabic zero stresses 
            5. Demote polysyllabic zero stresses
            6. Invalid line
    If rule 5 applies, then primary stress on a polysyllabic word had to be demoted
    Such words are contained in self._changed_words
    """

    BASE_PATTERN = (0,1,0,1,0,1,0,1,0,1)

    def __init__(self, tokens, DEV=False):
        self._tokens = tokens
        self._original_stress_patterns_per_token = []
        self._formatted_list_of_realized_stress_patterns = []
        self._unique_dict_of_realized_stress_patterns = {}
        self._is_valid_pattern = False
        self._current_state = 0
        self._rules_applied = []
        self._syllables_per_line = []
        self._changed_words = []

        if not DEV: self._main()


    def __str__(self):
        return f"{self._is_valid_pattern}, {len(self._rules_applied)}, {self._syllables_per_line}, {self._changed_words}"


    @property
    def line_facts(self):
        return {
            "rules_applied": len(self._rules_applied),
            "syllables_per_line": self._syllables_per_line,
            "changed_words": self._changed_words,
            "words_per_line": len(self._tokens),
        }

    
    def _get_transformed_words(self, comparisons):
        for comparison in comparisons:
            abstract,realized = comparison
            original = self._unique_dict_of_realized_stress_patterns[abstract]            
            lines = self._get_possible_stress_patterns_per_token(self._get_original_stress_patterns_per_token())
            realized = original
            iterations = len(realized[0])
            words = []
            for i in range(iterations):
                intermediate = []
                for line in lines:
                    intermediate.append(line[i])
                words.append(intermediate)

            def finder_real(word_variations, realized):
                if len(realized) <= 1: return False
                for word in word_variations:
                    if len(word) != len(realized): continue
                    for i in range(len(realized)):
                        if word[i] == 1:
                            if realized[i] == 1:
                                return False
                return True

            changed = [finder_real(words[i], realized[0][i]) for i in range(len(words)) ]
            res = [pair[1] for i,pair in enumerate(self._original_stress_patterns_per_token) if changed[i]]
            self._changed_words = res


    def _test_base_pattern(self):
        comparisons = []
        for potential,original in self._unique_dict_of_realized_stress_patterns.items():
            if len(potential) != len(self.BASE_PATTERN): continue
            comparison = [syl for i,syl in enumerate(potential) if i % 2 == 0 and syl in [0,2] or i % 2 == 1 and syl in [1,2] ]
            if len(comparison) == len(self.BASE_PATTERN):
                comparisons.append([potential, original])
        if comparisons: 
            if len(self._rules_applied) >= 5: self._get_transformed_words(comparisons)
            return True
        return False


    def _get_original_stress_patterns_per_token(self):
        return [(t.stress_patterns, t.token) for t in self._tokens]


    def _get_possible_stress_patterns_per_token(self, original_stress_patterns_per_token):
        """
        returns: List[Tuples(Lists)]
        """
        return list(product(*[pair[0] for pair in original_stress_patterns_per_token]))


    def _create_formatted_list_of_realized_stress_patterns(self, stress_patterns_per_token):
        """
        accepts: List[Tuples(Lists)]
        produces: 
            -adds on to self._formatted_list_of_realized_stress_patterns -- List[Dictionaries]
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
        self._formatted_list_of_realized_stress_patterns.extend(formatted_list_of_realized_stress_patterns)
        self._create_unique_dict_of_realized_stress_patterns()


    def _create_unique_dict_of_realized_stress_patterns(self):
        for entry in self._formatted_list_of_realized_stress_patterns:
            if self._unique_dict_of_realized_stress_patterns.get(entry["formatted"]):
                if entry["original"] not in self._unique_dict_of_realized_stress_patterns[entry["formatted"]]:
                    self._unique_dict_of_realized_stress_patterns[entry["formatted"]].append(entry["original"])
            else:
                self._unique_dict_of_realized_stress_patterns[entry["formatted"]] = [entry["original"]]


    def _get_syllables_per_line(self):
        for pattern in self._unique_dict_of_realized_stress_patterns:
            if len(pattern) not in self._syllables_per_line:
                self._syllables_per_line.append(len(pattern))


    def _is_valid_IP(self):
        self._get_syllables_per_line()
        if self._test_base_pattern():
            return True
        else:
            return self._fit_to_IP()


    def _fit_to_IP(self):
        """
        After the initial check:
            1. Demote compound-word stresses
            2. Demote monosyllable stresses
            3. Promote monosyllable stresses
            4. Promote polysyllabic zero stresses 
            5. Demote polysyllabic zero stresses
        """

        phases = {
            1: self._demote_compound_stress,
            2: self._demote_monosyllable_stress,
            3: self._promote_monosyllable_stresses,
            4: self._promote_polysyllabic_zero_stresses,
            5: self._demote_polysyllabic_primary_stresses,
        }
        self._rules_applied.append(phases[self._current_state].__name__)
        try:
            if phases[self._current_state]():
                return True
            else:
                return False
        except KeyError:
            self._current_state += 1
            self._rules_applied.append("FAILURE")
            return False


    def _promote_monosyllable_stresses(self):
        new_combinations = []
        monosyllable_nonprimary_count = 0
        line_i = 0
        for line in self._get_baseline_before_alteration():
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
        return self._check_validity_and_continue(new_combinations)


    @staticmethod
    def _create_demoted_compound_variations(word):
        word_stress_variations = []
        for i,syllable in enumerate(word):
            if syllable == 1:
                word_copy = [*word]
                word_copy[i] = 2
                word_stress_variations.append(word_copy)
                continue
        return word_stress_variations


    def _demote_compound_stress(self):
        new_combinations = []
        primary_count = 0
        for line in self._get_baseline_before_alteration():
            for word in line:
                for syllable in word:
                    if syllable == 1:
                        primary_count += 1
                    if primary_count > 1:
                        word_stress_variations = self._create_demoted_compound_variations(word)
                        idx_word_in_line = line.index(word)
                        for word_stress_variation in word_stress_variations:
                            line_copy = [w for w in line]
                            line_copy[idx_word_in_line] = word_stress_variation
                            line_copy = tuple(line_copy)
                            new_combinations.append(line_copy)
                primary_count = 0
            new_combinations.append(line)
        return self._check_validity_and_continue(new_combinations)


    def _demote_monosyllable_stress(self):
        """
        Works on a List[Tuples(Lists)]
        Creates a new List[Tuples(Lists)]

        Only demotes possibles in weak position
        """
        new_combinations = []
        monosyllable_primary_count = 0
        line_i = 0
        for line in self._get_baseline_before_alteration():
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
        return self._check_validity_and_continue(new_combinations)


    def _promote_polysyllabic_zero_stresses(self):
        """
        check if the word requires more than one stress
        can promote appropriate 0s to 2s
        """
        new_combinations = []
        for line in self._get_baseline_before_alteration():
            cg = CombinationsGraph([line], [0,2], True, 0)
            single_combinations = cg.new_combinations
            for single_combination in single_combinations:
                new_combinations.append(single_combination)

        return self._check_validity_and_continue(new_combinations)


    def _demote_polysyllabic_primary_stresses(self):
        new_combinations = []
        for line in self._get_baseline_before_alteration():
            cg = CombinationsGraph([line], [2, 1], False, 1)
            single_combinations = cg.new_combinations
            for single_combination in single_combinations:
                new_combinations.append(single_combination)

        return self._check_validity_and_continue(new_combinations)


    def _get_baseline_before_alteration(self):
        return (l for line in self._unique_dict_of_realized_stress_patterns.values() for l in line)


    def _check_validity_and_continue(self, new_combinations):
        self._create_formatted_list_of_realized_stress_patterns(new_combinations)
        self._current_state += 1
        self._is_valid_pattern = self._is_valid_IP()
        return self._is_valid_pattern


    def _main(self):
        self._tokens = [t for t in self._tokens if t.token not in ["th'", "t'"]]  # remove elided "the"
        self._original_stress_patterns_per_token = self._get_original_stress_patterns_per_token()
        possible_stress_patterns_per_token = self._get_possible_stress_patterns_per_token(self._original_stress_patterns_per_token)
        self._is_valid_pattern = self._check_validity_and_continue(possible_stress_patterns_per_token)
        
