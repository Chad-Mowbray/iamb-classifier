import re

from regularize import regularize as reg
from utils import args_logger


class SpellingNormalizer():
    """
    Accepts a word token which is not in the cmudict
    Checks:
        -Old spelling
        -Brittish spelling
        -Archaic 2P verb endings
        -Abbreviations with apostrophes
    """

    def __init__(self, unknown_word, uk_us_dict):
        self.unknown_word = unknown_word
        self.uk_us_dict = uk_us_dict
        self.modernized_word = []
        self.apostrophe_position = ''
        self.has_apostrophe = False
        self.modernized = ''

        self._main()
        # print("SpellingNormalizer instance created")

    def _local_list(self):
        print("_local_list called")
        local_list = {
            "o’er": "or"
        }
        return local_list.get(self.unknown_word, None)


    # @args_logger
    def _get_modernized_spelling(self):
        print("#### get modernized spelling called", self.unknown_word, len(self.unknown_word) )
        # self._apostrophe_check()
        print("#### after apostrophe checcked", self.unknown_word )
        self.modernized = reg.modernize(self.unknown_word) or self._brittish_converter() or self._local_list()
        print("$$$ modernized spelling", self.modernized)
        self._apostrophe_check()

        if self.modernized is None:
            self._old_fashioned_check()
            self._handle_not_found()
        else:
            self.modernized_word = [self.modernized, self.has_apostrophe, self.apostrophe_position]
        print("modernized_word: ", self.modernized_word)

    
    def _brittish_converter(self):
        if self.unknown_word in self.uk_us_dict:
            # print("BRITTISH"*50)
            return self.uk_us_dict[self.unknown_word]

    
    def _old_fashioned_check(self):
        if self.unknown_word.endswith("est") or self.unknown_word.endswith('eth') and len(self.unknown_word) > 5:
            self.modernized = self.unknown_word[:-3]


    def _handle_not_found(self):
        if self.unknown_word[0] == "'":
            self.modernized_word = [self._handle_initial_apostrophe(), self.has_apostrophe, "initial"]
        elif self.unknown_word[-1] =="'":
            self.modernized_word = [self._handle_final_apostrophe(), self.has_apostrophe, "final"]
        elif "'" in self.unknown_word[1:-2]:
            self.modernized_word = [self._handle_medial_apostrophe(), self.has_apostrophe, "medial"]
        else:
            self.modernized_word = [self.modernized, self.has_apostrophe, '']


    def _apostrophe_check(self):
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


    def _handle_medial_apostrophe(self): # TODO: make more robust
        return re.sub("'", "e", self.unknown_word)


    def _handle_initial_apostrophe(self):
        return self.unknown_word[1:]
    

    def _handle_final_apostrophe(self):
        # return self.unknown_word[:-1]
        return self.unknown_word


    def _main(self):
        self._get_modernized_spelling()



