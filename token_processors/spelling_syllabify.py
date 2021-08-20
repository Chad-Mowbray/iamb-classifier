import re
from copy import deepcopy
from nltk import pos_tag

class SpellingSyllabifier:
    """
    If a token is not in the dictionary,
    Syllabify a word based only on its spelling
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
        self.token = token
        self.syllable_count = 0
        self.modified_word = ''
        self.tentative_phonemes = [[]]
        self.reduced_syllables = 0

        self.main()

    
    def get_syllable_count(self):
        word = self.check_endings()
        word = self.check_special_cases(word)
        syllables = [w for w in word if w in self.VOWELS]
        self.syllable_count = len(syllables)
        print(self.syllable_count)

    def find_multiple(self, regex, word, rev=False):
        res = re.finditer(regex, word)
        indicies = [m.start() + 1 for m in res]
        indicies = indicies[::-1] if rev else indicies
        for idx in indicies:
            word = word[:idx] + word[idx + 1:]
            self.reduced_syllables += 1
        return word

    def find_single(self, letter, word):
        idx = word.rindex(letter)
        word = word[:idx] + word[idx + 1:]
        self.reduced_syllables += 1
        return word

    def check_endings(self):
        word = self.token

        if re.search(self.REGEX["EST"], word):
            word = self.find_single("e", word)
            return word

        if re.search(self.REGEX["IZE"], word):
            word = self.find_single("e", word)
            return word

        if re.search(self.REGEX["IAN"], word):
            word = self.find_single("i", word)
            return word

        if re.search(self.REGEX["IES"], word):
            word = self.find_single("e", word)
            return word
       
        if re.search(self.REGEX["SES"], word):
            return word

        if re.search(self.REGEX["E"], word):
            word = self.find_single("e", word)
            return word

        if re.search(self.REGEX["ION"], word)  and len(word) > 4:
            word = self.find_single("i", word)
            return word

        if re.search(self.REGEX["ED"], word)  and len(word) >= 4:
            word = self.find_single("e", word)
            return word

        return word


    def check_special_cases(self, word=None):
        word = word if word else self.token
    
        if re.search(self.REGEX["AU"], word):
            word = self.find_multiple(self.REGEX["AU"], word)
            return self.check_special_cases(word)

        if re.search(self.REGEX["AI"], word):
            word = self.find_multiple(self.REGEX["AI"], word)
            return self.check_special_cases(word)

        if re.search(self.REGEX["QU"], word):
            word = self.find_multiple(self.REGEX["QU"], word)
            return self.check_special_cases(word)

        if re.search(self.REGEX["AE"], word):
            word = self.find_multiple(self.REGEX["AE"], word, rev=True)
            return self.check_special_cases(word)

        if re.search(self.REGEX["DOUBLE"], word):
            word = self.find_multiple(self.REGEX["DOUBLE"], word)
            return self.check_special_cases(word)

        if re.search(self.REGEX["OU"], word):
            word = self.find_multiple(self.REGEX["OU"], word)
            return self.check_special_cases(word)

        if re.search(self.REGEX["EY"], word):
            word = self.find_multiple(self.REGEX["EY"], word)
            return self.check_special_cases(word)

        if re.search(self.REGEX["YV"], word):
            word = self.find_multiple(self.REGEX["YV"], word)
            return self.check_special_cases(word)

        if re.search(self.REGEX["EA"], word):
            word = self.find_multiple(self.REGEX["EA"], word)
            return self.check_special_cases(word)

        if re.search(self.REGEX["UI"], word):
            word = self.find_multiple(self.REGEX["UI"], word)
            return self.check_special_cases(word)

        if re.search(self.REGEX["OY"], word):
            word = self.find_multiple(self.REGEX["OY"], word)
            return self.check_special_cases(word)

        # print("^^^^^^^^^^^", word)
        self.modified_word = word
        return self.modified_word

    
    def simple_stressor(self, restore_syllables=0):
        count = self.syllable_count
        if count == 1:
            return [[self.DUMMY_STRESSED]]
        else:
            return [[self.DUMMY_STRESSED if i == self.syllable_count - 2 else self.DUMMY_UNSTRESSED for i in range(self.syllable_count + restore_syllables) ]]


    #TODO
    def complicated_stressor(self, POS, restore_syllables=0):
        if POS == "V" or any([self.token.endswith(ending) for ending in ["est", "eth", "ise", "ize"] ]):
            # initial stress 
            return [[self.DUMMY_STRESSED if i == 0 else self.DUMMY_UNSTRESSED for i in range(self.syllable_count + restore_syllables) ]]
        if POS in ["N", "J"]:
            # final stress 
            return [[self.DUMMY_STRESSED if i == self.syllable_count - 1 else self.DUMMY_UNSTRESSED for i in range(self.syllable_count + restore_syllables) ]]

    
    def check_ed(self, phonemes):
        print("check_ed called")
        print(phonemes, self.token)

        if self.token.endswith("ed") and len(self.token) > 4:
            print("\tnot a short word")
            antepenult_letter = self.token[-3]
            if antepenult_letter not in "aeiou":
                phonemes_copy = deepcopy(phonemes[0])
                print("\t", antepenult_letter, phonemes_copy)
                phonemes_copy.insert(-1,'EH0')
                print("\t", phonemes_copy)
                phonemes.append(phonemes_copy)
                self.reduced_syllables -= 1
        return phonemes

    
    def check_vowel_cluster(self, phonemes):
        print("check vowel clusters called")
        print(phonemes, self.token)

        if re.search(self.REGEX["EOU"], self.token):
            print("eou found...")
            phonemes_len = len(phonemes[0])
            reduced_phonemes = [self.DUMMY_STRESSED if i == 0 else self.DUMMY_UNSTRESSED for i in range(phonemes_len - 1) ]
            print(reduced_phonemes)
            phonemes.append(reduced_phonemes)
        if re.search(self.REGEX["EON"], self.token):
            print("eon found...")
            reduced_phonemes = [self.DUMMY_STRESSED if i == 0 else self.DUMMY_UNSTRESSED for i in range(2) ]
            phonemes.append(reduced_phonemes)
        if re.search(self.REGEX["VLV"], self.token):
            phonemes_len = len(phonemes[0])
            reduced_phonemes = [self.DUMMY_STRESSED if i == 0 else self.DUMMY_UNSTRESSED for i in range(phonemes_len - 1) ]
            print(reduced_phonemes)
            phonemes.append(reduced_phonemes)

        return phonemes


    def create_phoneme_repr(self):
        """
        Check POS, if none, use simple_stressor, otherwise, use complicated_stressor
        """

        tag = pos_tag([self.token])[0][1]
        print("****************", tag)
        if tag.startswith("V") or any([self.token.endswith(ending) for ending in ["est", "eth", "ise", "ize"] ]): #or tag.startswith("N") or tag.startswith("J") 
            self.tentative_phonemes = self.complicated_stressor(tag[0])
            if self.token.endswith('ed'):
                print("ends with ed...", self.tentative_phonemes)
                self.tentative_phonemes = self.check_ed(self.tentative_phonemes)
            if self.modified_word:
                print(self.tentative_phonemes)
                print(self.complicated_stressor(tag[0]))
                self.tentative_phonemes.append(self.complicated_stressor(tag[0], self.reduced_syllables)[0])
        else:
            self.tentative_phonemes = self.simple_stressor()
            if self.token.endswith('ed'):
                print("ends with ed else...", self.tentative_phonemes)
                self.tentative_phonemes = self.check_ed(self.tentative_phonemes)
                print("ends with ed else 2...", self.tentative_phonemes)
            if self.modified_word:
                self.tentative_phonemes.append(self.simple_stressor(self.reduced_syllables)[0])


    def final_reduction_check(self):
        print("final reduction check called")
        with_vowel_cluster = self.check_vowel_cluster(self.tentative_phonemes)
        self.tentative_phonemes = with_vowel_cluster



    def main(self):
        print("spelling syllabify started with:", self.token)
        self.get_syllable_count()
        self.create_phoneme_repr()
        self.final_reduction_check()



if __name__ == "__main__":
    from pprint import pprint

    # casque
    # upborne


    # words = ["quality", "inspections", "aeneidae", "look", "question", "thought", "thou", "linsey-woolsey", "pixie", "pixies", "yea", "treat", "galilaean", "harbingered", "yeoman"]

    # res = []
    # for word in words:
    #     ss = SpellingSyllabifier(word)
    #     res.append([word, ss.modified_word, ss.syllable_count])
    # pprint(res)

    ss = SpellingSyllabifier("latian")
    print(ss.token, ss.modified_word, ss.syllable_count, ss.tentative_phonemes)
    print(ss.tentative_phonemes)