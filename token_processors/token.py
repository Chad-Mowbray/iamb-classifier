from token_processors.spelling import SpellingNormalizer
from utils.logger import args_logger
from utils.representer import RepresenterMixin
from token_processors.compounds import Compounds
from token_processors.phoneme_fsm import PhonemeFSM

from syllabify.syllabify import syllabify, pprint

from re import search


class Token(RepresenterMixin):
    """
    Accepts a word
    Represents features of a token
    """
    PRIMARY_STRESS = "1"
    NO_STRESS = "0"
    SECONDARY_STRESS = "2"

    def __init__(self, token, dicts):
        self.token = token
        self.d = dicts
        self.stress_patterns = []
        self.syllable_counts = set()
        self.modified_token = ''
        self.phoneme_reprs = []
        self.syllabification = []

        self.main()
        # print("Token instance created: ", self.token)

    def __str__(self):
        return f"Token instance: {self.token}"
    
    def __repr__(self):
        return str(self)

    def __call__(self, *args, **kwargs):
        return {
            "original_token": self.token,
            "modified_token": self.modified_token,
            "stress_patterns": self.stress_patterns,
            "syllable_counts": self.syllable_counts,
            "phoneme_reprs": self.phoneme_reprs,
            "syllabifications": self.syllabifications
        }


    # @args_logger
    def handle_compounds(self, phoneme_reprs):
        updated_phoneme_reprs = []
        for phoneme_repr in phoneme_reprs:
            primary_stress_indicies = [i for i,phon in enumerate(phoneme_repr) if self.PRIMARY_STRESS in phon ]
            if len(primary_stress_indicies) > 1:
                for idx in reversed(primary_stress_indicies):
                    phoneme_repr_copy = [phon for phon in phoneme_repr]
                    # print("copy: ",phoneme_repr_copy)
                    phoneme_repr_copy[idx] = phoneme_repr_copy[idx][:-1] + self.SECONDARY_STRESS
                    updated_phoneme_reprs.append(phoneme_repr_copy)
                updated_phoneme_reprs.append(phoneme_repr)
                # print("updated compound repr: ", updated_phoneme_reprs)
                return updated_phoneme_reprs
        # print("unmodified compound repr: ", phoneme_reprs)
        return phoneme_reprs


    # @args_logger
    def get_phonemes_from_dict(self):
        token = self.token
        # print("token: ", token)
        fsm = PhonemeFSM(token)
        # print("new fsm: ", id(fsm))
        # phoneme_reprs = fsm.dispatch()
        phoneme_reprs = fsm.final_phoneme_repr
        # print("phoneme_reprs: ", phoneme_reprs)
        self.phoneme_reprs = self.handle_compounds(phoneme_reprs)
        # print(fsm)
        self.modified_token = fsm.normalized_spelling
       

    # @args_logger
    def get_syllable_count(self):
        counts = []
        for syllabification in self.syllabifications:
            counts.append(len(syllabification))
        self.syllable_count = counts


    # @args_logger
    def get_syllabification(self):
        syllabifications = []
        for stress_repr in self.phoneme_reprs:
            # print("&&&&&&&&&&&&&&&&&&&&&&&&& get_syllabification: ", stress_repr)
            syllabified = pprint(syllabify(stress_repr, 0)).split('.')
            # print("########### syllabified: ", syllabified)
            syllabifications.append(syllabified)
        self.syllabifications = syllabifications


    # @args_logger
    def get_stress_patterns(self):
        stress_patterns = []
        # print(self.syllabifications)
        for syllabification in self.syllabifications:
            # pattern = [1 if self.PRIMARY_STRESS in syl else 0 for syl in syllabification]
            pattern = [int(search(r'[12]', syl).group()) if search(r'[12]', syl) else 0 for syl in syllabification]
            # print(pattern)
            if sum(pattern) > 1:
                x = 2
                # print("multiple stress...")
            stress_patterns.append(pattern)
        self.stress_patterns = stress_patterns
  

    # @args_logger
    def main(self):
        # print("in Token, token:", self.token)
        self.get_phonemes_from_dict()
        self.get_syllabification()
        self.get_syllable_count()
        self.get_stress_patterns()
        # print(self())



