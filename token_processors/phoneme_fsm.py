from utils.dicts import DictsSingleton
from token_processors.spelling import SpellingNormalizer
from token_processors.compounds import Compounds
from token_processors.spelling_syllabify import SpellingSyllabifier
from copy import deepcopy
import re


class PhonemeFSM():

    def __init__(self, token):
        self.initial_token = token
        self.dicts = DictsSingleton()
        self.cmudict = self.dicts.cmudict
        self.normalized_spelling = ''
        self.has_apostrophe = False
        self.apostrophe_position = ''
        self.is_compound = [False, False]
        self.final_phoneme_repr = []
        self.left_compound = ''
        self.right_compound = ''
        self.count = 0
        self.stress_assigned_diy = False

        self.lookup()


    def check_ed(self, phonemes):
        print("check_ed called")
        print(phonemes, self.initial_token)

        if self.initial_token.endswith("ed") and len(self.initial_token) > 4 and not self.is_compound[0]:
            print("left compound: ", self.left_compound)
            print(self.is_compound)
            print("\tnot a short word")
            antepenult_letter = self.initial_token[-3]
            if antepenult_letter not in "aeiou":
                phonemes_copy = deepcopy(phonemes[0])
                print("\t", antepenult_letter, phonemes_copy)
                phonemes_copy.insert(-1,'EH0')
                print("\t", phonemes_copy)
                phonemes.append(phonemes_copy)
        print("check_ed result: ", phonemes)
        return phonemes
        

    def lookup(self, called_by_normalize=False, compound_token=None):
        # print("compound_token: ", compound_token)
        token = self.normalized_spelling if self.normalized_spelling else self.initial_token
        token = compound_token if compound_token else token
        print("lookup called with: ", token )
        # print("token: ", token)
        try:
            phonemes = self.cmudict.get(token, None)
            # print("___________________________________________________", phonemes)
            if phonemes is None: raise KeyError()
            phonemes = self.check_ed(phonemes)
            print(phonemes)
            self.handle_success(phonemes)
        except KeyError:
            if called_by_normalize and self.count < 1:
                print('will call compound')
                self.count += 1
                self.compound()
            elif called_by_normalize and self.count > 2:
                print('will call handle failure')
                self.handle_failure()
            else:
                print('will call normalize')
                self.count += 1
                self.normalize(token)

    
    def normalize(self, token):
        print("normalize called")
        # if any(self.is_compound): self.
        spelling_normalized, has_apostrophe, apostrophe_position = SpellingNormalizer(token).modernized_word
        if has_apostrophe: self.has_apostrophe = True
        if spelling_normalized: self.normalized_spelling = spelling_normalized
        if apostrophe_position: self.apostrophe_position = apostrophe_position
        if spelling_normalized:
            # print("spelling normalized: ", spelling_normalized, "has_apostrophe:", self.has_apostrophe)
            self.lookup(called_by_normalize=True)
        else:
            if any(self.is_compound):
                self.lookup(called_by_normalize=True)
            else:
                self.compound()
        

    def compound(self):
        print("compound called...")
        token = self.normalized_spelling if self.normalized_spelling else self.initial_token
        compound = Compounds(token, self.dicts.words, self.dicts.lemmatizer).find_compound_in_wordlist()
        # print("compound: ", compound)
        if compound:
            left, right = compound[0], compound[1]
            # print(left, right)

            print("left about to be checked with:", left)
            self.is_compound[0] = True
            self.lookup(compound_token=left)
            print("left checked")
            if self.stress_assigned_diy: return

            print("right about to be checked with:", right)
            self.is_compound[1] = True
            self.lookup(compound_token=right)
            print("right checked")

        else:
            # self.count += 1
            # self.apostrophe()
            self.handle_failure()


    def apostrophe(self, phonemes):
        if not self.has_apostrophe: return phonemes
        print("apostrophe called")
        pop_position = 0 if self.apostrophe_position == "initial" else -1
        print(self.apostrophe_position)
        phonemes_copy = deepcopy(phonemes)
        reduced = []
        for word in phonemes_copy:
            filtered = [i for i,v in enumerate(word) if v[-1].isdigit()]
            word.pop(filtered[pop_position])
            reduced.append(word)
        return reduced


    def diy_stress_assignment(self):
        print("God help you...")

        # clear out compound residue
        self.is_compound = [False, False]
        self.left_compound = None
        self.right_compound = None
        
        spelling_syllabifier = SpellingSyllabifier(self.initial_token)
        tentative_phonemes = spelling_syllabifier.tentative_phonemes
        print("tentative_phonemes: ", tentative_phonemes)
        print(self.is_compound, self.left_compound, self.right_compound)
        self.stress_assigned_diy = True

        self.handle_success(tentative_phonemes)


    def check_stress_reduction(self, phonemes):
        #TODO make more general -> two consecutive stresses can be reduced
        """
        [['K', 'AA1', 'N', 'JH', 'ER0', 'IH0', 'NG']] ->
        [['K', 'AA1', 'N', 'JH', 'ER0', 'IH0', 'NG'], ['K', 'AA1', 'N', 'JH', 'IH0', 'NG']]
        """
        if self.stress_assigned_diy: return phonemes
        print("check stress reduction called with: ", phonemes)
        new_phonemes = []
        for word in phonemes:
            print(word)
            for i in range(len(word) - 1):
                print(word[i])
                if word[i][-1].isdigit() and word[i+1][-1].isdigit():
                    print(word[i], word[i+1])
                    word_copy = deepcopy(word)
                    word_copy.pop(i + 1)
                    new_phonemes.append(word_copy)
                    break
            new_phonemes.append(word)
        print(new_phonemes)
        return new_phonemes
            

    def handle_success(self, phonemes):
        print("handle_success called with: ", phonemes)

        phonemes = self.check_stress_reduction(phonemes)

        if self.stress_assigned_diy: 
            print("handle_success stress assigned diy: ", phonemes)
            print("handle_success stress assigned diy final_phoneme_repr before: ", self.final_phoneme_repr)
            self.final_phoneme_repr = []
            if self.final_phoneme_repr:
                return
            else:
                self.final_phoneme_repr = phonemes
            print("handle_success stress assigned diy final_phoneme_repr after: ", self.final_phoneme_repr)
            return

        if any(self.is_compound):
            print("checking compound: ", self.is_compound)
            if self.is_compound[0]:
                print("left compound: ", phonemes)
                self.left_compound = phonemes
                self.is_compound[0] = False
                # print("left_compound:", self.left_compound)
            if self.is_compound[1]:
                print("right compound: ", phonemes)
                self.right_compound = phonemes
                self.is_compound[1] = False
                # print("right_compound:", self.right_compound)
        if self.left_compound and self.right_compound:
            print("both left and right are valid")
            # print("Will be a valid compound")
            # TODO: should final form be one or two words?
            # self.final_phoneme_repr = [self.left_compound[0] + self.right_compound[0]]
            combined = [lt + rt for lt in self.left_compound for rt in self.right_compound]
            self.final_phoneme_repr = self.apostrophe(combined)
            print("final compound repr:!!!! ", self.final_phoneme_repr)
            return

        elif self.has_apostrophe:
            reduced_phonemes = self.apostrophe(phonemes)
            self.final_phoneme_repr = reduced_phonemes
            return
        
        self.final_phoneme_repr = phonemes
        
        print("end of handle_success")
        print(self.final_phoneme_repr)
        return

        
    def handle_failure(self):
        # print("handle_failure called...")
        print("*" * 80, "Unable to parse token ", self.initial_token, "final_phoneme_repr", self.final_phoneme_repr)
        self.diy_stress_assignment()
        return

