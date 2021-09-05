import os
import pickle
from collections import Counter, OrderedDict
from copy import deepcopy



class ModelBase:
    """
    Base class for preparing features
    """

    def __init__(self):
        self.accented_words_file = os.path.join(os.path.dirname(__file__), "master_word_list.pickle")
        self.ordered_accented_words = {}
        self.counter_dicts = []
        self.other_features = []
        self.all_period_features = []
        self.features = OrderedDict()


    def get_accented_words(self):
        with open(self.accented_words_file, 'rb') as f:
            accented_words = pickle.load(f)
            return accented_words


    def create_accented_word_dict(self):
        accented_words = self.get_accented_words()
        unordered_accented_words = Counter(accented_words)
        ordered_accented_words = OrderedDict(unordered_accented_words)
        self.ordered_accented_words = ordered_accented_words


    def create_fresh_word_dict(self):
        ordered_accented_words_copy = deepcopy(self.ordered_accented_words)
        fresh_word_dict = OrderedDict({k:0 for k in ordered_accented_words_copy})
        return fresh_word_dict


    def get_sections_per_period(self):
        counter_dict = self.features["counter_dict"]
        rules_avg = self.features["rules_avg"]
        words_per_line = self.features["words_per_line"]
        avg_syllables_per_line = self.features["avg_syllables_per_line"]
        rule_0 = self.features["rule_0"]
        rule_1 = self.features["rule_1"]
        rule_2 = self.features["rule_2"]
        rule_3 = self.features["rule_3"]
        rule_4 = self.features["rule_4"]
        rule_5 = self.features["rule_5"]
        rule_6 = self.features["rule_6"]
        self.counter_dicts.append(counter_dict)
        self.other_features = [
                                rules_avg, 
                                words_per_line, 
                                avg_syllables_per_line, 
                                rule_0, 
                                rule_1, 
                                rule_2, 
                                rule_3, 
                                rule_4, 
                                rule_5, 
                                rule_6
                                ] 


    def create_accented_word_feature(self):
        for sect in self.counter_dicts:
            sect = sorted([word for word in sect])
            sect_dict = OrderedDict(Counter(sect))
            sect_combined = OrderedDict()
            for k,v in self.ordered_accented_words.items():
                if k in sect_dict:
                    sect_combined[k] = 1
                else:
                    sect_combined[k] = 0
            one_hot_sect = [[float(v) for v in sect_combined.values()]]
            one_hot_sect[0].extend(self.other_features)

        return one_hot_sect


    def combine_all_period_features(self):
        pass


    def main(self):
        pass