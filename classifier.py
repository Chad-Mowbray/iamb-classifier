import pickle
import os
import numpy as np
from collections import Counter, OrderedDict
from sklearn.naive_bayes import GaussianNB, MultinomialNB, ComplementNB, BernoulliNB, CategoricalNB
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn import svm
from sklearn.linear_model import SGDClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn import metrics
from copy import deepcopy
from random import shuffle

import sys
sys.path.append("../")
from dataprep import RawFileProcessor
from runner import Runner



class Classifier:

    PERIODS = (
        "elizabethan",
        "neoclassical",
        "romantic",
        "victorian"
    )
    SECTION_LENGTH = 500

    def __init__(self, accented_words_file):
        # self.period_pickle_files = period_pickle_files
        self.accented_words_file = accented_words_file
        self.ordered_accented_words = {}
        self.counter_dicts = []
        self.other_features = []
        self.all_period_features = []

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

    
    def get_sections_per_period(self, period, iterations=1):
        print('get sections per period started...')

        filename = os.path.join(os.path.dirname(__file__), f"poems/{period}_poems.txt")
        rfp = RawFileProcessor(filename)
        contents = rfp.cleaned_contents

        for j in range(iterations):
            shuffle(contents)
            sectioned_contents = []
            sections = []
            for i,line in enumerate(contents):
                if i == 0: continue
                # print(line.rstrip("\n"))
                sections.append(line.rstrip("\n"))
                if i % self.SECTION_LENGTH == 0:
                    sectioned_contents.append(sections)
                    sections = []

            for i,section in enumerate(sectioned_contents):
                r = Runner(section)
                # genre = f"neoclassical_test-{j}-{i}"
                features = r.initial_process_contents(period) ######################TODO
                counter_dict = features["counter_dict"]
                rules_avg = features["rules_avg"]
                words_per_line = features["words_per_line"]
                avg_syllables_per_line = features["avg_syllables_per_line"]
                self.counter_dicts.append(counter_dict)
                self.other_features = [rules_avg, words_per_line, avg_syllables_per_line] #######################
                print("other_features: ", self.other_features)


    def create_accented_word_feature(self, period):
        print('create accebted word feature started...')

        period_features = []
        for i,sect in enumerate(self.counter_dicts):
            sect = sorted([word for word in sect])
            sect_dict = OrderedDict(Counter(sect))
            sect_combined = OrderedDict()
            for k,v in self.ordered_accented_words.items():
                if k in sect_dict:
                    sect_combined[k] = 1
                else:
                    sect_combined[k] = 0
            one_hot_sect = [[float(v) for v in sect_combined.values()]]
            one_hot_sect[0].extend(self.other_features) #######################
            one_hot_sect.append(period)
            period_features.append(one_hot_sect)

        return period_features
        # get features for all periods, then combine them, then do train-test split


    def reset(self):
        print('reset started...')
        self.counter_dicts = []
        self.other_features = []


    def combine_all_period_features(self):
        print('combine all period features started...')
        flattened_all_period_features = [sect for period in self.all_period_features for sect in period]
        # print(flattened_all_period_features)
        # raise Exception()
        shuffle(flattened_all_period_features)
        return flattened_all_period_features


    def get_train_test_split(self, flattened_all_period_features):
        print('get train test split started...')
        X = [x[0] for x in flattened_all_period_features]
        y = [x[1] for x in flattened_all_period_features]
        # print("asdf")
        # print(X)
        # print("fdsa")
        # print(y)

        size = len(X)
        if size != len(y): raise Exception("X and y not same len")
        test_split_point = size // 4
        X_train = X[test_split_point:]
        y_train = y[test_split_point:]
        X_train_np = np.array(X_train)
        y_train_np = np.array(y_train)

        X_test = X[:test_split_point]
        y_test = y[:test_split_point]
        X_test_np = np.array(X_test)
        y_test_np = np.array(y_test)

        return {
            "X_test_np": X_test_np,
            "y_test_np": y_test_np,
            "X_train_np": X_train_np,
            "y_train_np": y_train_np
        }


    def train_model(self, train_test):
        print('train model started...')
        models = [GaussianNB, svm.LinearSVC, MultinomialNB, ComplementNB, RandomForestClassifier, GradientBoostingClassifier, MLPClassifier]
        names = ["gaussiannb", "linearSVC",  "MultinomialNB", "ComplementNB", "RandomForestClassifier", "GradientBoostingClassifier", "MLPClassifier"]
        for i,model in enumerate(models):
            print(str(model))
            print( len(train_test["X_train_np"]), len(train_test["y_train_np"]) )
            # if model == "RandomForestClassifier":
            #     test_model = RandomForestClassifier(max_depth=4)
            # else:
            test_model = model()
            test_model.fit(train_test["X_train_np"], train_test["y_train_np"])
            with open(f'{names[i]}_test-trained-model.pickle', 'wb') as f:
                pickle.dump(test_model, f)


    def test_model(self, train_test):
        print('test model started...')
        models = ["gaussiannb", "linearSVC",  "MultinomialNB", "ComplementNB", "RandomForestClassifier", "GradientBoostingClassifier", "MLPClassifier"]
        for model in models:
            with open(f"{model}_test-trained-model.pickle", 'rb') as f:
                print(f"{model}...", "\n")
                test_model = pickle.load(f)
                predicted = test_model.predict(train_test["X_test_np"])
                print(metrics.classification_report(train_test["y_test_np"], predicted))
                print(metrics.confusion_matrix(train_test["y_test_np"], predicted))


    def main(self):
        print('main started...')
        self.create_accented_word_dict()
        for period in self.PERIODS:
            print("on period: ", period)
            self.get_sections_per_period(period)
            period_features = self.create_accented_word_feature(period)
            self.all_period_features.append(period_features)
            self.reset()
        flattened_all_period_features = self.combine_all_period_features()
        train_test = self.get_train_test_split(flattened_all_period_features)
        self.train_model(train_test)
        self.test_model(train_test)
        


if __name__ == "__main__":
    # files = ["elizabetha.pickle", "neoclassic.pickle", "romantic_p.pickle", "victorian_.pickle"]
    c = Classifier("accented_words.txt")

