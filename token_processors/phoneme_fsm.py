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
        self.is_compound = [False, False]
        self.final_phoneme_repr = [[]]
        self.left_compound = ''
        self.right_compound = ''
        self.count = 0

        self.lookup()



    def lookup(self, called_by_normalize=False, compound_token=None):
        # print("lookup called")
        # print("compound_token: ", compound_token)
        token = self.normalized_spelling if self.normalized_spelling else self.initial_token
        token = compound_token if compound_token else token
        # print("token: ", token)
        try:
            phonemes = self.cmudict.get(token, None)
            # print("___________________________________________________", phonemes)
            if phonemes is None: raise KeyError()
            self.handle_success(phonemes)
        except KeyError:
            if called_by_normalize and self.count == 0:
                self.count += 1
                self.compound()
            elif called_by_normalize and self.count > 1:
                self.handle_failure()
            else:
                self.normalize(token)


    
    def normalize(self, token):
        # print("normalize called")
        # if any(self.is_compound): self.
        spelling_normalized, has_apostrophe = SpellingNormalizer(token).modernized_word
        if has_apostrophe: self.has_apostrophe = True
        if spelling_normalized: self.normalized_spelling = spelling_normalized
        if spelling_normalized:
            # print("spelling normalized: ", spelling_normalized, "has_apostrophe:", self.has_apostrophe)
            self.lookup(called_by_normalize=True)
        else:
            if any(self.is_compound):
                self.lookup(called_by_normalize=True)
            else:
                self.compound()
        


    def compound(self):
        # print("compound called...")
        token = self.normalized_spelling if self.normalized_spelling else self.initial_token
        compound = Compounds(token, self.dicts.words, self.dicts.lemmatizer).find_compound_in_wordlist()
        # print(compound)
        if compound:
            left, right = compound[0], compound[1]
            # print(left, right)

            self.is_compound[0] = True
            self.lookup(compound_token=left)
            # print("left checked")

            self.is_compound[1] = True
            self.lookup(compound_token=right)
            # print("right checked")

        else:
            # self.count += 1
            # self.apostrophe()
            self.handle_failure()


    def apostrophe(self, phonemes):
        phonemes_copy = deepcopy(phonemes)
        reduced = []
        for word in phonemes_copy:
            filtered = [i for i,v in enumerate(word) if v[-1].isdigit()]
            word.pop(filtered[-1])
            reduced.append(word)
        return reduced

    def diy_stress_assignment(self):
        print("God help you...")
        spelling_syllabifier = SpellingSyllabifier(self.initial_token)
        tentative_phonemes = spelling_syllabifier.tentative_phonemes
        self.handle_success(tentative_phonemes)



    def handle_success(self, phonemes):
        # print("handle_success called with: ", phonemes)

        if any(self.is_compound):
            # print("checking compound: ", self.is_compound)
            if self.is_compound[0]:
                self.left_compound = phonemes
                self.is_compound[0] = False
                # print("left_compound:", self.left_compound)
            if self.is_compound[1]:
                self.right_compound = phonemes
                self.is_compound[1] = False
                # print("right_compound:", self.right_compound)
        if self.left_compound and self.right_compound:
            # print("Will be a valid compound")
            # TODO: should final form be one or two words?
            self.final_phoneme_repr = [self.left_compound[0] + self.right_compound[0]]
            return

        elif self.has_apostrophe:
            reduced_phonemes = self.apostrophe(phonemes)
            self.final_phoneme_repr = reduced_phonemes
            return
        
        self.final_phoneme_repr = phonemes
        
        # print("end of handle_success")
        # print(self.final_phoneme_repr)
        return

        

    def handle_failure(self):
        # print("handle_failure called...")
        print("*" * 80, "Unable to parse token ", self.initial_token, self.final_phoneme_repr)
        self.diy_stress_assignment()
        return


