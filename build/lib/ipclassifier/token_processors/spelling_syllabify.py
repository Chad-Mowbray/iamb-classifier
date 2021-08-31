import re
from copy import deepcopy
from nltk import pos_tag



class SpellingSyllabifier:
    """
    A last resort if a word token cannot be found elsewhere
    Syllabifies a word based only on its spelling
    Ridiculously expandable
    """

    VOWELS = "aeiouy"
    DUMMY_STRESSED = "AH1"
    DUMMY_UNSTRESSED = "AH0"
    REGEX = {
        # Endings
        "IES": r'ies?$',
        "ION": r'[st]{1}ions?$',
        "ED": r'[^aeiou]ed$',
        "EST": r'.{2,}est$',
        "IZE": r'i[sz]es?$',
        "E": r'[^aeio]es?$',
        "SES": r'[sz]es$',
        "IAN": r'ianS?$',
        # Non-Endings
        "QU": r'qu',
        "AE": r'ae',
        "DOUBLE": r'([eiouy])\1',  # no double a
        "OU": r'ou',
        "EY": r'ey\W?',
        "YV": r'y[aeiou]',
        "EA": r'ea',
        "AI": r'ai',
        "AU": r'au',
        "UI": r'ui',
        "OY": r'oy',
        # Others
        "EOU": r'eou',
        "EON": r'eon',
        "VLV": r'[aeiou]{1}[vwrl][aeiou]{1}'
    }

    def __init__(self, token):
        self.tentative_phonemes = [[]]
        
        self._token = token
        self._syllable_count = 0
        self._modified_word = ''
        self._reduced_syllables = 0

        self._main()

    
    def _get_syllable_count(self):
        word = self._check_endings()
        word = self._check_special_cases(word)
        syllables = [w for w in word if w in self.VOWELS]
        self._syllable_count = len(syllables)


    def _find_multiple(self, regex, word, rev=False):
        res = re.finditer(regex, word)
        indicies = [m.start() + 1 for m in res]
        indicies = indicies[::-1] if rev else indicies
        for idx in indicies:
            word = word[:idx] + word[idx + 1:]
            self._reduced_syllables += 1
        return word


    def _find_single(self, letter, word):
        idx = word.rindex(letter)
        word = word[:idx] + word[idx + 1:]
        self._reduced_syllables += 1
        return word


    def _check_endings(self):
        word = self._token

        if re.search(self.REGEX["EST"], word):
            word = self._find_single("e", word)
            return word

        if re.search(self.REGEX["IZE"], word):
            word = self._find_single("e", word)
            return word

        if re.search(self.REGEX["IAN"], word):
            word = self._find_single("i", word)
            return word

        if re.search(self.REGEX["IES"], word):
            word = self._find_single("e", word)
            return word
       
        if re.search(self.REGEX["SES"], word):
            return word

        if re.search(self.REGEX["E"], word):
            word = self._find_single("e", word)
            return word

        if re.search(self.REGEX["ION"], word)  and len(word) > 4:
            word = self._find_single("i", word)
            return word

        if re.search(self.REGEX["ED"], word)  and len(word) >= 4:
            word = self._find_single("e", word)
            return word
        return word


    def _check_special_cases(self, word=None):
        word = word if word else self._token
    
        if re.search(self.REGEX["AU"], word):
            word = self._find_multiple(self.REGEX["AU"], word)
            return self._check_special_cases(word)

        if re.search(self.REGEX["AI"], word):
            word = self._find_multiple(self.REGEX["AI"], word)
            return self._check_special_cases(word)

        if re.search(self.REGEX["QU"], word):
            word = self._find_multiple(self.REGEX["QU"], word)
            return self._check_special_cases(word)

        if re.search(self.REGEX["AE"], word):
            word = self._find_multiple(self.REGEX["AE"], word, rev=True)
            return self._check_special_cases(word)

        if re.search(self.REGEX["DOUBLE"], word):
            word = self._find_multiple(self.REGEX["DOUBLE"], word)
            return self._check_special_cases(word)

        if re.search(self.REGEX["OU"], word):
            word = self._find_multiple(self.REGEX["OU"], word)
            return self._check_special_cases(word)

        if re.search(self.REGEX["EY"], word):
            word = self._find_multiple(self.REGEX["EY"], word)
            return self._check_special_cases(word)

        if re.search(self.REGEX["YV"], word):
            word = self._find_multiple(self.REGEX["YV"], word)
            return self._check_special_cases(word)

        if re.search(self.REGEX["EA"], word):
            word = self._find_multiple(self.REGEX["EA"], word)
            return self._check_special_cases(word)

        if re.search(self.REGEX["UI"], word):
            word = self._find_multiple(self.REGEX["UI"], word)
            return self._check_special_cases(word)

        if re.search(self.REGEX["OY"], word):
            word = self._find_multiple(self.REGEX["OY"], word)
            return self._check_special_cases(word)
        self._modified_word = word
        return self._modified_word

    
    def _simple_stressor(self, restore_syllables=0):
        count = self._syllable_count
        if count == 1:
            return [[self.DUMMY_STRESSED]]
        else:
            return [[self.DUMMY_STRESSED if i == self._syllable_count - 2 else self.DUMMY_UNSTRESSED for i in range(self._syllable_count + restore_syllables) ]]


    def _complicated_stressor(self, POS, restore_syllables=0):
        if POS == "V" or any([self._token.endswith(ending) for ending in ["est", "eth", "ise", "ize"] ]):
            return [[self.DUMMY_STRESSED if i == 0 else self.DUMMY_UNSTRESSED for i in range(self._syllable_count + restore_syllables) ]]
        if POS in ["N", "J"]:
            return [[self.DUMMY_STRESSED if i == self._syllable_count - 1 else self.DUMMY_UNSTRESSED for i in range(self._syllable_count + restore_syllables) ]]

    
    def _check_ed(self, phonemes):
        if self._token.endswith("ed") and len(self._token) > 4:
            antepenult_letter = self._token[-3]
            if antepenult_letter not in "aeiou":
                phonemes_copy = deepcopy(phonemes[0])
                phonemes_copy.insert(-1,'EH0')
                phonemes.append(phonemes_copy)
                self._reduced_syllables -= 1
        return phonemes

    
    def _check_vowel_cluster(self, phonemes):
        if re.search(self.REGEX["EOU"], self._token):
            phonemes_len = len(phonemes[0])
            reduced_phonemes = [self.DUMMY_STRESSED if i == 0 else self.DUMMY_UNSTRESSED for i in range(phonemes_len - 1) ]
            phonemes.append(reduced_phonemes)
        if re.search(self.REGEX["EON"], self._token):
            reduced_phonemes = [self.DUMMY_STRESSED if i == 0 else self.DUMMY_UNSTRESSED for i in range(2) ]
            phonemes.append(reduced_phonemes)
        if re.search(self.REGEX["VLV"], self._token):
            phonemes_len = len(phonemes[0])
            reduced_phonemes = [self.DUMMY_STRESSED if i == 0 else self.DUMMY_UNSTRESSED for i in range(phonemes_len - 1) ]
            phonemes.append(reduced_phonemes)

        return phonemes


    def _create_phoneme_repr(self):
        """
        Check POS, if none, use simple_stressor, otherwise, use complicated_stressor
        """

        tag = pos_tag([self._token])[0][1]
        if tag.startswith("V") or any([self._token.endswith(ending) for ending in ["est", "eth", "ise", "ize"] ]): #or tag.startswith("N") or tag.startswith("J") 
            self.tentative_phonemes = self._complicated_stressor(tag[0])
            if self._token.endswith('ed'):
                self.tentative_phonemes = self._check_ed(self.tentative_phonemes)
            if self._modified_word:
                self.tentative_phonemes.append(self._complicated_stressor(tag[0], self._reduced_syllables)[0])
        else:
            self.tentative_phonemes = self._simple_stressor()
            if self._token.endswith('ed'):
                self.tentative_phonemes = self._check_ed(self.tentative_phonemes)
            if self._modified_word:
                self.tentative_phonemes.append(self._simple_stressor(self._reduced_syllables)[0])


    def _final_reduction_check(self):
        with_vowel_cluster = self._check_vowel_cluster(self.tentative_phonemes)
        self.tentative_phonemes = with_vowel_cluster


    def _main(self):
        self._get_syllable_count()
        self._create_phoneme_repr()
        self._final_reduction_check()
