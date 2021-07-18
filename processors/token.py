
from utils.logger import args_logger
from utils.logger import args_logger
from utils.representer import RepresenterMixin

from syllabify.syllabify import syllabify, pprint


class Token(RepresenterMixin):
    """
    Accepts a word
    Represents features of a token
    """
    PRIMARY_STRESS = "1"
    NO_STRESS = "0"
    SECONDARY_STRESS = "2"

    def __init__(self, token, cmudict):
        self.token = token
        self.d = cmudict
        self.stress_pos = []
        self.syllable_count = set()
        self.modified_token = ''
        self.stress_reprs = []
        self.syllabification = []

        self.main()

    def __str__(self):
        return f"Token instance: {self.token}"

    def __call__(self, *args, **kwargs):
        return {
            "original_token": self.token,
            "modified_token": self.modified_token,
            "stress_position": self.stress_pos,
            "syllable_count": self.syllable_count,
            "stress_repr": self.stress_reprs,
            "syllabification": self.syllabification
        }

    @args_logger
    def get_stress_from_dict(self):
        try:
            self.stress_reprs = self.d[self.token]
            count = self.get_syllable_count(self.stress_reprs)
            self.syllable_count = count
        except KeyError:
            return "not found"

    @classmethod
    def get_syllable_count(cls, stress_reprs):
        print(stress_reprs)
        counts = []
        for stress_repr in stress_reprs:
            count = 0
            for phoneme in stress_repr:
                if phoneme[-1].isdigit():
                    if phoneme[-1] == cls.PRIMARY_STRESS:
                        count += 1
            counts.append(count)
        return set(counts)


    def get_syllabification(self):
        syllabification = []
        for stress_repr in self.stress_reprs:
            syllabified = pprint(syllabify(stress_repr, 0)).split('.')
            syllabification.append(syllabified)
        self.syllabification = syllabification


    @args_logger
    def main(self):
        self.get_stress_from_dict()
        self.get_syllabification()



