from utils.logger import args_logger
from utils.representer import RepresenterMixin
import re

from regularize import regularize as reg

class SpellingNormalizer(RepresenterMixin):

    def __init__(self, unknown_word):
        self.unknown_word = unknown_word
        self.modernized_word = []
        self.apostrophe_position = ''

        self.main()
        # print("SpellingNormalizer instance created")

    # @args_logger
    def get_modernized_spelling(self):
        modernized = reg.modernize(self.unknown_word)
        print("$$$ modernized spelling", modernized)

        has_apostrophe = False
        if "'" in self.unknown_word[0:-1]: #if "'" in self.unknown_word[1:-1]:
            has_apostrophe = True
            print("has an apostrophe: ", self.unknown_word)
            if self.unknown_word[0] == "'":
                self.apostrophe_position = "initial"
            else:
                self.apostrophe_position = "medial"
        if modernized is None:
            if self.unknown_word[0] == "'":
                self.modernized_word = [self.handle_initial_apostrophe(), has_apostrophe, "initial"]
            elif "'" in self.unknown_word[1:-2]:
                self.modernized_word = [self.handle_non_initial_apostrophe(), has_apostrophe, "medial"]
            else:
                self.modernized_word = [modernized, has_apostrophe, '']
        else:
            self.modernized_word = [modernized, has_apostrophe, self.apostrophe_position]
        print("modernized_word: ", self.modernized_word)


    def handle_non_initial_apostrophe(self): # TODO: make more robust
        # print("handle_non_initial_apostrophe called")
        return re.sub("'", "e", self.unknown_word)

    def handle_initial_apostrophe(self):
        return self.unknown_word[1:]

    def main(self):
        self.get_modernized_spelling()



