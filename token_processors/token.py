from re import search

from utils import args_logger
from syllabify import syllabify, syllabify_pprint

from .phoneme_fsm import PhonemeFSM



class Token():
    """
    Accepts a word
    Represents features of a token
    """
    
    PRIMARY_STRESS = "1"
    NO_STRESS = "0"
    SECONDARY_STRESS = "2"

    def __init__(self, token, dicts):
        self.token = token
        self.dicts = dicts
        self.stress_patterns = []
        self.modified_token = ''
        self.phoneme_reprs = []
        self.syllabification = []

        self._main()


    def __str__(self):
        return f"Token instance: {self.token}"

    def __call__(self, *args, **kwargs):
        return {
            "original_token": self.token,
            "modified_token": self.modified_token,
            "stress_patterns": self.stress_patterns,
            "phoneme_reprs": self.phoneme_reprs,
            "syllabifications": self.syllabifications
        }


    # @args_logger
    def _get_phonemes_from_dict(self):
        token = self.token
        # print("token: ", token)
        fsm = PhonemeFSM(token, self.dicts)
        # print("new fsm: ", id(fsm))
        # phoneme_reprs = fsm.dispatch()
        phoneme_reprs = fsm.final_phoneme_repr
        print("phoneme_reprs from Token: ", phoneme_reprs)
        self.phoneme_reprs = phoneme_reprs #self.handle_compounds(phoneme_reprs)
        # print(fsm)
        self.modified_token = fsm.normalized_spelling
       

    # @args_logger
    def _get_syllabification(self):
        syllabifications = []
        for stress_repr in self.phoneme_reprs:
            # print("&&&&&&&&&&&&&&&&&&&&&&&&& get_syllabification: ", stress_repr)
            syllabified = syllabify_pprint(syllabify(stress_repr, 0)).split('.')
            print("########### syllabified: ", syllabified)
            syllabifications.append(syllabified)
        self.syllabifications = syllabifications


    # @args_logger
    def _get_stress_patterns(self):
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
    def _main(self):
        # print("in Token, token:", self.token)
        self._get_phonemes_from_dict()
        self._get_syllabification()
        # self.get_syllable_count()
        self._get_stress_patterns()
        # print(self())



