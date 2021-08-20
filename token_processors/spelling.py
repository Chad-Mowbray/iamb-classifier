from utils.logger import args_logger
from utils.representer import RepresenterMixin
import re

from regularize import regularize as reg

class SpellingNormalizer(RepresenterMixin):

    def __init__(self, unknown_word, uk_us_dict):
        self.unknown_word = unknown_word
        self.uk_us_dict = uk_us_dict
        self.modernized_word = []
        self.apostrophe_position = ''
        self.has_apostrophe = False
        self.modernized = ''

        self.main()
        # print("SpellingNormalizer instance created")

    def local_list(self):
        print("local_list called")
        local_list = {
            "o’er": "or"
        }
        return local_list.get(self.unknown_word, None)


    # @args_logger
    def get_modernized_spelling(self):
        print("#### get modernized spelling called", self.unknown_word, len(self.unknown_word) )
        # self.apostrophe_check()
        print("#### after apostrophe checcked", self.unknown_word )
        self.modernized = reg.modernize(self.unknown_word) or self.brittish_converter() or self.local_list()
        print("$$$ modernized spelling", self.modernized)
        self.apostrophe_check()

        if self.modernized is None:
            self.old_fashioned_check()
            self.handle_not_found()
        else:
            self.modernized_word = [self.modernized, self.has_apostrophe, self.apostrophe_position]
        print("modernized_word: ", self.modernized_word)

    
    def brittish_converter(self):
        if self.unknown_word in self.uk_us_dict:
            # print("BRITTISH"*50)
            return self.uk_us_dict[self.unknown_word]

    
    def old_fashioned_check(self):
        if self.unknown_word.endswith("est") or self.unknown_word.endswith('eth') and len(self.unknown_word) > 5:
            self.modernized = self.unknown_word[:-3]


    def handle_not_found(self):
        if self.unknown_word[0] == "'":
            self.modernized_word = [self.handle_initial_apostrophe(), self.has_apostrophe, "initial"]
        elif self.unknown_word[-1] =="'":
            self.modernized_word = [self.handle_final_apostrophe(), self.has_apostrophe, "final"]
        elif "'" in self.unknown_word[1:-2]:
            self.modernized_word = [self.handle_medial_apostrophe(), self.has_apostrophe, "medial"]
        else:
            self.modernized_word = [self.modernized, self.has_apostrophe, '']


    def apostrophe_check(self):
        print("apostrophe check called")
        print(self.unknown_word, len(self.unknown_word))
        if self.unknown_word[-1] == "'":
            self.has_apostrophe = True
            self.apostrophe_position = "final" 
        elif "'" in self.unknown_word[0:-1]: #if "'" in self.unknown_word[1:-1]:
            self.has_apostrophe = True
            print("has an apostrophe: ", self.unknown_word)
            if self.unknown_word[0] == "'":
                self.apostrophe_position = "initial"
            else:
                self.apostrophe_position = "medial"


    def handle_medial_apostrophe(self): # TODO: make more robust
        return re.sub("'", "e", self.unknown_word)


    def handle_initial_apostrophe(self):
        return self.unknown_word[1:]
    

    def handle_final_apostrophe(self):
        # return self.unknown_word[:-1]
        return self.unknown_word


    def main(self):
        self.get_modernized_spelling()



