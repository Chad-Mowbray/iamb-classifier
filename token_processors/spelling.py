from utils.logger import args_logger
from utils.representer import RepresenterMixin
import re

from regularize import regularize as reg

class SpellingNormalizer(RepresenterMixin):

    def __init__(self, unknown_word):
        self.unknown_word = unknown_word
        self.modernized_word = []

        self.main()
        # print("SpellingNormalizer instance created")

    # @args_logger
    def get_modernized_spelling(self):
        modernized = reg.modernize(self.unknown_word)
        # print("$$$ modernized spelling", modernized)

        has_apostrophe = False
        if "'" in self.unknown_word[1:]:
            has_apostrophe = True
        if modernized is None:
            if "'" in self.unknown_word[1:]:
                self.modernized_word = [self.handle_non_initial_apostrophe(), has_apostrophe]
            else:
                self.modernized_word = [modernized, has_apostrophe]
        else:
            self.modernized_word = [modernized, has_apostrophe]


    def handle_non_initial_apostrophe(self):
        return re.sub("'", "e", self.unknown_word)


    def main(self):
        self.get_modernized_spelling()



