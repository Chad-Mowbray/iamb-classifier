import pickle
import os
import numpy as np
from collections import Counter, OrderedDict
from copy import deepcopy



class Classifier:
    """
    Processes sample features to be consumed by the model
    Categorizes the sample
    """


    def __init__(self, accented_words_file, features):
        self.features = features
        self.accented_words_file = accented_words_file
        self.ordered_accented_words = {}
        self.counter_dicts = []
        self.other_features = []
        self.all_period_features = []
        self.guessed_period = ''

        self.main()


    def get_accented_words(self):
        print('get accented words started...')

        with open(self.accented_words_file, 'r') as f:
            accented_words = [word.rstrip("\n") for word in f.readlines()]
            return accented_words


    def create_accented_word_dict(self):
        print('create accented word dict started...')

        accented_words = self.get_accented_words()
        unordered_accented_words = Counter(accented_words)
        ordered_accented_words = OrderedDict(unordered_accented_words)
        self.ordered_accented_words = ordered_accented_words


    def create_fresh_word_dict(self):
        print('create fresh word dict started...')

        ordered_accented_words_copy = deepcopy(self.ordered_accented_words)
        fresh_word_dict = OrderedDict({k:0 for k in ordered_accented_words_copy})
        return fresh_word_dict

    
    def get_sections_per_period(self):
        print('get sections per period started...')

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
        print('create accebted word feature started...')

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
        print('combine all period features started...')
        flattened_all_period_features = [sect for period in self.all_period_features for sect in period]
        return np.array(flattened_all_period_features)


    def guess_period(self, flattened_all_period_features):
        filepath = os.path.join(os.path.dirname(__file__), "models/high-test_refined-ComplementNB_test-trained-model.pickle")
        with open(filepath, "rb") as f:
            model = pickle.load(f)
            self.guessed_period = model.predict(flattened_all_period_features)


    def main(self):
        print('main started...')
        self.create_accented_word_dict()
        self.get_sections_per_period()
        period_features = self.create_accented_word_feature()
        self.all_period_features.append(period_features)
        flattened_all_period_features = self.combine_all_period_features()
        self.guess_period(flattened_all_period_features)
        