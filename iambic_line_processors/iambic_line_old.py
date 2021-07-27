from itertools import product
from pprint import pprint



class IambicLine():

    BASE_PATTERN = (0,1,0,1,0,1,0,1,0,1)
    WORD_STRESS_PATTERNS = {
        2: ( [0,1], [1,0] ),
        3: ( [0,0,1], [0,1,0], [1,0,0] ),
        4: ( [0,0,0,1], [0,0,1,0], [0,1,0,0], [1,0,0,0] ),
        5: ( [0,0,0,0,1], [0,0,0,1,0], [0,0,1,0,0], [0,1,0,0,0], [1,0,0,0,0] ),
        6: ( [0,0,0,0,0,1], [0,0,0,0,1,0], [0,0,0,1,0,0], [0,0,1,0,0,0], [0,1,0,0,0,0], [1,0,0,0,0,0] )
    }

    
    def __init__(self, tokens):
        self.tokens = tokens
        self.base_stress_pattern = self.get_base_stress_pattern()
        self.round_1_complete = False
        self.round_2_complete = False

    def get_base_stress_pattern(self, tokens=None):
        tokens = tokens if tokens else self.tokens
        stresses = [(t.stress_patterns, t.token) for t in tokens]
        print(len(stresses), "stresses", stresses)
        return stresses

    def combinations_set(self, **kwargs):
        base_patterns = kwargs["base_patterns"] if kwargs.get("base_patterns") else self.get_base_stress_pattern(**kwargs)
        #TODO if 2 in base pattern, then it can be either a 0 or 1
        # should happen after other failures
        combos = list(product(*[pair[0] for pair in base_patterns]))
        self.combos = combos
        return self.combos

    def possible_stress_patterns(self, new_possibles=None):
        print("possible_stress_patterns: ", new_possibles)
        combos_list = []
        combinations_set = new_possibles if new_possibles else self.combinations_set()
        print("possible_stress_patterns, combinations_set: ", combinations_set)

        for c in combinations_set:
            f = tuple( s for w in c for s in w)
            line = {
                "formatted": f,
                "original": c
            }
            combos_list.append(line)
        self.combos_list = combos_list
        return self.combos_list

    def is_ip(self, possible_stress_pattern=None):
        print("checking if ip...")
        possible_stress_pattern = possible_stress_pattern if possible_stress_pattern else self.possible_stress_patterns()
        for s in possible_stress_pattern:
            simplified = [syl if syl in [0,1] else 1 for syl in s["formatted"]]
            print("####### simplified: ", simplified)
            if simplified == self.BASE_PATTERN:
                self.res = s
                self.get_closest_fit()
                return True

        if self.round_2_complete:
            print('round 2 is complete, returning False')
            return False
        else:
            print("GOTO fit_to_ip()")
            # return
            self.round_1_complete = True
            return self.fit_to_ip()


    def fit_to_ip(self):
        if self.round_1_complete:
            return self.try_promoting_secondary_stresses()
        elif self.round_2_complete:
            return self.try_alternate_stress_placement()


    def try_promoting_secondary_stresses(self):
            #TODO if 2 in base pattern, then it can be either a 0 or 1
            # should happen after other failures
            print("in try_promoting_secondary_stresses, base_stress_pattern: ", self.base_stress_pattern)
            combinations = self.combinations_set(base_patterns=self.base_stress_pattern)
            print("in try_promoting_secondary_stresses, combinations: ", combinations)

            new_combinations = [ tuple([ [val if val in [0,1] else 1 for val in combination[0] ] ],) for combination in combinations]

            new_possibles = self.possible_stress_patterns(new_possibles=new_combinations)
            print("in try_promoting_secondary_stresses, new_possibles: ", new_possibles)

            self.round_2_complete = True
            return self.is_ip(possible_stress_pattern=new_possibles)

            # new_combinations = [ [val if val in [0,1] else 1 for val in combination[0] ] for combination in combinations]
            # new_combinations = [ tuple([ [val if val in [0,1] else 1 for val in combination[0] ] ],) for combination in combinations]
            # print(new_combinations)
            # self.combinations_set(tokens=tokens)
            # raise Exception()
            # return self.is_ip(new_possibles=new_possibles)




    def try_alternate_stress_placement(self):
            possibles = self.combos
            new_possibles = []
            for c in possibles:
                for i,w in enumerate(c):
                    if len(w) > 1:
                        for variant in self.WORD_STRESS_PATTERNS[len(w)]:
                            c_copy = [w for w in c]
                            c_copy[i] = variant
                            new_possibles.append(c_copy)
            return self.is_ip(new_possibles=new_possibles)


    #TODO
    def get_closest_fit(self):
        # get the pattern(s) with the closest fit
        # to use as point of comparison for 'fitted' line
        pass
        print()
        # print(self.base_stress_pattern)
        # print(len(self.base_stress_pattern), "stresses end", self.base_stress_pattern)
        # print(self.res)
        final_stress_pattern = zip(self.res["original"], [pair[1] for pair in self.base_stress_pattern])
        # print(list(final_stress_pattern))
        return list(final_stress_pattern)
