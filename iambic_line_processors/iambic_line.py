from itertools import product
from pprint import pprint
from functools import cached_property
from itertools import combinations, combinations_with_replacement
from typing import final


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

    def get_base_stress_pattern(self, tokens=None):
        tokens = tokens if tokens else self.tokens
        stresses = [(t.stress_patterns, t.token) for t in tokens]
        # print(len(stresses), "stresses", stresses)
        return stresses

    def combinations_set(self, **kwargs):
        base_patterns = self.get_base_stress_pattern(**kwargs)
        combos = list(product(*[pair[0] for pair in base_patterns]))
        self.combos = combos
        return self.combos

    def possible_stress_patterns(self, new_possibles=None):
        combos_list = []
        combinations_set = new_possibles if new_possibles else self.combinations_set()
        for c in combinations_set:
            f = tuple( s for w in c for s in w)
            line = {
                "formatted": f,
                "original": c
            }
            combos_list.append(line)
        self.combos_list = combos_list
        # return combos_set


    def is_ip(self, **kwargs):
        self.possible_stress_patterns(**kwargs)
        for s in self.combos_list:
            if s["formatted"] == self.BASE_PATTERN:
                self.res = s
                self.get_closest_fit()
                return True
        else:
            print("GOTO fit_to_ip()")
            return self.fit_to_ip()


    def fit_to_ip(self):
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
        print(len(self.base_stress_pattern), "stresses end", self.base_stress_pattern)
        print(self.res)
        final_stress_pattern = zip(self.res["original"], [pair[1] for pair in self.base_stress_pattern])
        print(list(final_stress_pattern))
        return list(final_stress_pattern)
