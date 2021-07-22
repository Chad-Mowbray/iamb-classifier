
from processors.spelling import SpellingNormalizer
from utils.logger import args_logger
from utils.representer import RepresenterMixin
from processors.compounds import Compounds

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

    @args_logger
    def lookup(self, token):
        return self.d.cmudict[token]

    @args_logger
    def spelling_normalizer(self, token):
        spelling_normalizer = SpellingNormalizer(token)
        print("########## ", spelling_normalizer.modernized_word)
        return spelling_normalizer.modernized_word

    @args_logger
    def compound_checker(self, token):
        print('Checking if compound...')
        compound = Compounds(token, self.d.words, self.d.lemmatizer).find_compound_in_wordlist()
        if compound:
            pass
        print(compound)
        return compound if compound else "not found"

    @args_logger
    def handle_not_in_cmudict(self, token):
        spelling_normalized_token = self.spelling_normalizer(token)
        # if spelling_normalized_token:
        #     try:
        #         self.lookup(spelling_normalized_token)


    @args_logger
    def get_phonemes_from_dict(self, variant=None):
        try:
            token = variant if variant else self.token
            print("token: ", token)
            self.phoneme_reprs = self.lookup(token)
            self.modified_token = token if variant else ''
        except KeyError:
            print("key error")
            self.handle_not_in_cmudict(token)
            # spelling_normalizer = SpellingNormalizer(token)
            # print("########## ", spelling_normalizer.modernized_word)
            # if spelling_normalizer.modernized_word is None:
            #     print('Checking if compound...')
            #     compound = Compounds(token, self.d.words, self.d.lemmatizer).find_compound_in_wordlist()
            #     if compound:
            #         pass
            #     print(compound)
            #     return compound if compound else "not found"
            # else:
            #     print('retry')
            #     self.get_phonemes_from_dict(spelling_normalizer.modernized_word)


    @args_logger
    def get_syllable_count(self):
        counts = []
        for syllabification in self.syllabifications:
            counts.append(len(syllabification))
        self.syllable_count = counts


    @args_logger
    def get_syllabification(self):
        syllabifications = []
        for stress_repr in self.phoneme_reprs:
            syllabified = pprint(syllabify(stress_repr, 0)).split('.')
            syllabifications.append(syllabified)
        self.syllabifications = syllabifications

    @args_logger
    def get_stress_patterns(self):
        stress_patterns = []
        for syllabification in self.syllabifications:
            pattern = [1 if self.PRIMARY_STRESS in syl else 0 for syl in syllabification]
            stress_patterns.append(pattern)
        self.stress_patterns = stress_patterns
  

    @args_logger
    def main(self):
        self.get_phonemes_from_dict()
        self.get_syllabification()
        self.get_syllable_count()
        self.get_stress_patterns()



