import re
from ipclassifier.regularize import Regularize



class SpellingNormalizer():
    """
    Accepts a word token which is not in the cmudict
    Checks:
        -Old spelling
        -Brittish spelling
        -Archaic 2P verb endings
        -Abbreviations with apostrophes
    """

    def __init__(self, unknown_word, uk_us_dict, regularize_dicts):
        self._unknown_word = unknown_word
        self._uk_us_dict = uk_us_dict
        self._regularize_dicts = regularize_dicts
        self.modernized_word = []
        self._apostrophe_position = ''
        self._has_apostrophe = False
        self._modernized = ''

        self._main()


    def _local_list(self):
        local_list = {
            "o’er": "or"
        }
        return local_list.get(self._unknown_word, None)


    def _get_modernized_spelling(self):
        self._modernized = Regularize(self._regularize_dicts).modernize(self._unknown_word) or self._brittish_converter() or self._local_list()
        self._apostrophe_check()
        if self._modernized is None:
            self._old_fashioned_check()
            self._handle_not_found()
        else:
            self.modernized_word = [self._modernized, self._has_apostrophe, self._apostrophe_position]

    
    def _brittish_converter(self):
        if self._unknown_word in self._uk_us_dict:
            return self._uk_us_dict[self._unknown_word]

    
    def _old_fashioned_check(self):
        if self._unknown_word.endswith("est") or self._unknown_word.endswith('eth') and len(self._unknown_word) > 5:
            self._modernized = self._unknown_word[:-3]


    def _handle_not_found(self):
        if len(self._unknown_word) == 0:
            self.modernized_word = [self._modernized, self._has_apostrophe, '']
        elif self._unknown_word[0] == "'":
            self.modernized_word = [self._handle_initial_apostrophe(), self._has_apostrophe, "initial"]
        elif self._unknown_word[-1] =="'":
            self.modernized_word = [self._handle_final_apostrophe(), self._has_apostrophe, "final"]
        elif "'" in self._unknown_word[1:-2]:
            self.modernized_word = [self._handle_medial_apostrophe(), self._has_apostrophe, "medial"]
        else:
            self.modernized_word = [self._modernized, self._has_apostrophe, '']


    def _apostrophe_check(self):
        if len(self._unknown_word) <= 1:
            return
        if self._unknown_word[-1] == "'":
            self._has_apostrophe = True
            self._apostrophe_position = "final" 
        elif "'" in self._unknown_word[0:-1]:
            self._has_apostrophe = True
            if self._unknown_word[0] == "'":
                self._apostrophe_position = "initial"
            else:
                self._apostrophe_position = "medial"


    def _handle_medial_apostrophe(self): # TODO: make more robust
        return re.sub("'", "e", self._unknown_word)


    def _handle_initial_apostrophe(self):
        return self._unknown_word[1:]
    

    def _handle_final_apostrophe(self):
        return self._unknown_word


    def _main(self):
        self._get_modernized_spelling()



