from processors.spelling import SpellingNormalizer
from utils.logger import args_logger
from utils.representer import RepresenterMixin
from processors.compounds import Compounds
from processors.phoneme_fsm import PhonemeFSM

from syllabify.syllabify import syllabify, pprint


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

    def __str__(self):
        return f"Token instance: {self.token}"

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
                    phoneme_repr_copy[idx] = phoneme_repr_copy[idx][:-1] + self.SECONDARY_STRESS
                    updated_phoneme_reprs.append(phoneme_repr_copy)
                return updated_phoneme_reprs
        return phoneme_reprs


    # @args_logger
    def get_phonemes_from_dict(self):
        token = self.token
        print("token: ", token)
        fsm = PhonemeFSM(token)
        phoneme_reprs = fsm.dispatch()
        self.phoneme_reprs = self.handle_compounds(phoneme_reprs)
        print(fsm)
        self.modified_token = fsm.spelling_normalized
       

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
            syllabified = pprint(syllabify(stress_repr, 0)).split('.')
            syllabifications.append(syllabified)
        self.syllabifications = syllabifications


    # @args_logger
    def get_stress_patterns(self):
        stress_patterns = []
        for syllabification in self.syllabifications:
            pattern = [1 if self.PRIMARY_STRESS in syl else 0 for syl in syllabification]
            if sum(pattern) > 1:
                print("multiple stress...")
            stress_patterns.append(pattern)
        self.stress_patterns = stress_patterns
  

    # @args_logger
    def main(self):
        self.get_phonemes_from_dict()
        self.get_syllabification()
        self.get_syllable_count()
        self.get_stress_patterns()



