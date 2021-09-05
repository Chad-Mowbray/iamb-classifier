from collections import Counter, OrderedDict
from sklearn.naive_bayes import GaussianNB, MultinomialNB, ComplementNB
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn import svm
from sklearn.neural_network import MLPClassifier
from sklearn import metrics
from random import shuffle
import pickle
import os
import numpy as np
from .model_base import ModelBase
from ipclassifier.dataprep import RawFileProcessor



class ModelTrainer(ModelBase):

    PERIODS = (
        "15th-Century",
        "16th-Century",
        "17th-Century",
        "18th-Century",
        "19th-Century-(Romantic)",
        "19th-Century-(Victorian)"
    )
    SECTION_LENGTH = 100

    def __init__(self, feature_runner ,accented_words_file="master_word_list.pickle"):
        super().__init__()
        self.accented_words_file = os.path.join(os.path.dirname(__file__), accented_words_file)
        self.feature_runner = feature_runner

        self.main()

    
    def get_sections_per_period(self, period, iterations=1):
        print('get sections per period started...')

        filename = os.path.join(os.path.dirname(__file__), f"poems/_{period}.txt")
        rfp = RawFileProcessor(filename)
        contents = rfp.cleaned_contents

        for j in range(iterations):
            shuffle(contents)
            sectioned_contents = []
            sections = []
            for i,line in enumerate(contents):
                if i == 0: continue
                sections.append(line.rstrip("\n"))
                if i % self.SECTION_LENGTH == 0:
                    sectioned_contents.append(sections)
                    sections = []

            for i,section in enumerate(sectioned_contents):
                r = self.feature_runner(section)
                features = r.initial_process_contents(period)
                counter_dict = features["counter_dict"]
                rules_avg = features["rules_avg"]
                words_per_line = features["words_per_line"]
                avg_syllables_per_line = features["avg_syllables_per_line"]
                rule_0 = features["rule_0"]
                rule_1 = features["rule_1"]
                rule_2 = features["rule_2"]
                rule_3 = features["rule_3"]
                rule_4 = features["rule_4"]
                rule_5 = features["rule_5"]
                rule_6 = features["rule_6"]
                self.counter_dicts.append(counter_dict)
                self.other_features = [rules_avg, words_per_line, avg_syllables_per_line, rule_0, rule_1, rule_2, rule_3, rule_4, rule_5, rule_6] 


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
            one_hot_sect[0].extend(self.other_features)
            one_hot_sect.append(period)
            period_features.append(one_hot_sect)

        return period_features


    def reset(self):
        print('reset started...')
        self.counter_dicts = []
        self.other_features = []


    def combine_all_period_features(self):
        print('combine all period features started...')
        flattened_all_period_features = [sect for period in self.all_period_features for sect in period]
        shuffle(flattened_all_period_features)
        return flattened_all_period_features


    def get_train_test_split(self, flattened_all_period_features):
        print('get train test split started...')
        X = [x[0] for x in flattened_all_period_features]
        y = [x[1] for x in flattened_all_period_features]

        size = len(X)
        print("size y", len(y), y)
        if size != len(y): raise Exception("X and y not same len")
        test_split_point = size // 10
        X_train = X[test_split_point:]
        y_train = y[test_split_point:]
        X_train_np = np.array(X_train)
        y_train_np = np.array(y_train)

        X_test = X[:test_split_point]
        y_test = y[:test_split_point]
        X_test_np = np.array(X_test)
        y_test_np = np.array(y_test)

        # print("saving train test pickle...")
        # with open("train_test_data.pickle", "wb") as f:
        #     pickle.dump({
        #     "X_test_np": X_test_np,
        #     "y_test_np": y_test_np,
        #     "X_train_np": X_train_np,
        #     "y_train_np": y_train_np
        # }, f)

        return {
            "X_test_np": X_test_np,
            "y_test_np": y_test_np,
            "X_train_np": X_train_np,
            "y_train_np": y_train_np
        }


    def train_model(self, train_test):
        print('train model started...')
        # models = [MultinomialNB, ComplementNB, MLPClassifier]
        # names = ["MultinomialNB", "ComplementNB", "MLPClassifier"]
        # for i,model in enumerate(models):
        #     print(str(model))
        #     print( len(train_test["X_train_np"]), len(train_test["y_train_np"]) )

        #     if names[i] == "ComplementNB":
        #         test_model = model(alpha=2.0)
        #     if names[i] == "MLPClassifier":
        #         test_model = model(activation="identity", alpha=1e-08, solver="lbfgs", hidden_layer_sizes=(100,), max_iter=2000)
        #     test_model = model()
        #     test_model.fit(train_test["X_train_np"], train_test["y_train_np"])
        test_model = ComplementNB(alpha=2.0)
        test_model.fit(train_test["X_train_np"], train_test["y_train_np"])
        with open(f'garbage.pickle', 'wb') as f:
            pickle.dump(test_model, f)


    def test_model(self, train_test):
        with open(f"garbage.pickle", 'rb') as f:
            test_model = pickle.load(f)
            predicted = test_model.predict(train_test["X_test_np"])
            print(metrics.classification_report(train_test["y_test_np"], predicted))
            print(metrics.confusion_matrix(train_test["y_test_np"], predicted))
            print(metrics.accuracy_score(train_test["y_test_np"], predicted))

            print("Accuracy on training set: {:.3f}".format(test_model.score(train_test["X_train_np"], train_test["y_train_np"])))
            print("Accuracy on test set: {:.3f}".format(test_model.score(train_test["X_test_np"], train_test["y_test_np"])))


    def main(self):
        print('main started...')
        self.create_accented_word_dict()
        for period in self.PERIODS:
            print("on period: ", period)
            self.get_sections_per_period(period)
            period_features = self.create_accented_word_feature(period)
            self.all_period_features.append(period_features)
            print("len all period features", len(self.all_period_features))
            self.reset()
        flattened_all_period_features = self.combine_all_period_features()
        print("len flattened all period features", len(flattened_all_period_features))
        train_test = self.get_train_test_split(flattened_all_period_features)
        self.train_model(train_test)
        self.test_model(train_test)
        

