from re import search
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
        self._dicts = dicts
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


    def _get_phonemes_from_dict(self):
        token = self.token
        fsm = PhonemeFSM(token, self._dicts)
        phoneme_reprs = fsm.final_phoneme_repr
        self.phoneme_reprs = phoneme_reprs
        self.modified_token = fsm.normalized_spelling
       

    def _get_syllabification(self):
        syllabifications = []
        for stress_repr in self.phoneme_reprs:
            syllabified = syllabify_pprint(syllabify(stress_repr, 0)).split('.')
            syllabifications.append(syllabified)
        self.syllabifications = syllabifications


    def _get_stress_patterns(self):
        stress_patterns = []
        for syllabification in self.syllabifications:
            pattern = [int(search(r'[12]', syl).group()) if search(r'[12]', syl) else 0 for syl in syllabification]
            if sum(pattern) > 1:
                x = 2
            stress_patterns.append(pattern)
        self.stress_patterns = stress_patterns
  

    def _main(self):
        self._get_phonemes_from_dict()
        self._get_syllabification()
        self._get_stress_patterns()



