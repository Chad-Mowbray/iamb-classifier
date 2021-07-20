from utils.logger import args_logger
from utils.representer import RepresenterMixin

from regularize import regularize as reg

class SpellingNormalizer(RepresenterMixin):

    def __init__(self, unknown_word):
        self.unknown_word = unknown_word
        self.modernized_word = ''

        self.main()

    @args_logger
    def get_modernized_spelling(self):
        modernized = reg.modernize(self.unknown_word)
        print(modernized)
        self.modernized_word = modernized


    def main(self):
        self.get_modernized_spelling()