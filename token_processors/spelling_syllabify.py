import re

class SpellingSyllabifier:
    """
    If a token is not in the dictionary,
    Syllabify a word based only on its spelling
    """

    VOWELS = "aeiouy"
    DUMMY_STRESSED = "AH1"
    DUMMY_UNSTRESSED = "AH0"

    def __init__(self, token):
        self.token = token
        self.syllable_count = 0
        self.tentative_phonemes = [[]]

        self.main()

    
    def get_syllable_count(self):
        word = self.check_special_cases()
        syllables = [w for w in word if w in self.VOWELS]
        self.syllable_count = len(syllables)
        print(self.syllable_count)


    def check_special_cases(self, word=None):
        word = word if word else self.token
        if re.search(r'qu', word):
            res = re.finditer(r'qu', word)
            qu_indicies = [m.start() + 1 for m in res]
            for qu_index in qu_indicies:
                word = word[:qu_index] + word[qu_index + 1:]
        elif re.search(r'[st]{1}ions?$', word)  and len(word) > 4:
            i_index = word.rindex('i')
            return self.check_special_cases(word[:i_index] + word[i_index + 1:])
        elif re.search(r'ae', word):
            res = re.finditer(r'ae', word)
            ae_indicies = [m.start() + 1 for m in res]
            for ae_idx in ae_indicies[::-1]:
                word = word[:ae_idx] + word[ae_idx + 1:]
            print("ae fixed: ", word)
            return self.check_special_cases(word)
        elif re.search(r'([aeiouy])\1', word):
            res = re.finditer(r'([aeiouy])\1', word)
            double_vowel_indicies = [m.start() + 1 for m in res]
            for double_vowel_idx in double_vowel_indicies:
                word = word[:double_vowel_idx] + word[double_vowel_idx + 1:]
            print("double vowel fixed: ", word)
            return self.check_special_cases(word)
        elif re.search(r'ou', word):
            res = re.finditer(r'ou', word)
            ou_dipthong_indicies = [m.start() + 1 for m in res]
            for ou_dipthong_idx in ou_dipthong_indicies:
                word = word[:ou_dipthong_idx] + word[ou_dipthong_idx + 1:]
            print("ou fixed: ", word)
            return self.check_special_cases(word)
        elif re.search(r'ey\W?', word):
            res = re.finditer(r'ey\W?', word)
            ey_dipthong_indicies = [m.start() + 1 for m in res]
            for ey_dipthong_idx in ey_dipthong_indicies:
                word = word[:ey_dipthong_idx] + word[ey_dipthong_idx + 1:]
            print("ey fixed: ", word)
            return self.check_special_cases(word)
        elif re.search(r'ies?$', word):
            i_index = word.rindex('e')
            return self.check_special_cases(word[:i_index] + word[i_index + 1:])
        print("^^^^^^^^^^^", word)
        return word

    
    def simple_stressor(self):
        count = self.syllable_count
        if count == 1:
            return [[self.DUMMY_STRESSED]]
        else:
            return [[self.DUMMY_STRESSED if i == self.syllable_count - 2 else self.DUMMY_UNSTRESSED for i in range(self.syllable_count) ]]


    #TODO
    def complicated_stressor(self):
        pass


    def create_phoneme_repr(self):
        self.tentative_phonemes = self.simple_stressor()


    def main(self):
        self.get_syllable_count()
        self.create_phoneme_repr()