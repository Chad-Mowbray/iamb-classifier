import itertools


class CombinationsBaseMixin:
    """
    Creates new possible lines of IP given multiple versions of a token
    """

    def __init__(self, lines, product_possibles, is_odd_postition, target_stress):
        self._lines = lines
        self._product_possibles = product_possibles
        self._is_odd_position = 1 if is_odd_postition else 0
        self._target_stress = target_stress


    def _get_word_combinations(self, word, zero_stress_idxs):
        possible_words = []
        for possible in itertools.product(self._product_possibles,repeat=len(zero_stress_idxs)):
            word_copy = [s for s in word]
            for i,p in enumerate(possible):
                for j,s in enumerate(word_copy):
                    if j != zero_stress_idxs[i]:
                        word_copy[j] = s
                    else:
                        word_copy[j] = p            
            possible_words.append(word_copy)
        return possible_words


    def _get_line_combinations(self):
        line_pos = 0
        for line in self._lines:
            temp_line = []
            for word in line:
                if len(word) < 2:
                    line_pos += len(word)
                    temp_line.append([word])
                    continue
                zero_stress_idxs = [i for i,syl in enumerate(word) if (i + line_pos) % 2 == self._is_odd_position and syl == self._target_stress]
                if zero_stress_idxs:
                    word_combinations = self._get_word_combinations(word, zero_stress_idxs)
                    temp_line.append(word_combinations)
                else:
                    temp_line.append([word])
                line_pos += len(word)
            line_pos = 0
            self._build_graph(temp_line)