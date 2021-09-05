import pickle
import os
import numpy as np
from .model_base import ModelBase



class Classifier(ModelBase):
    """
    Processes sample features to be consumed by the model
    Categorizes the sample
    """

    def __init__(self, features, accented_words_file="master_word_list.pickle"):
        super().__init__()
        self.features = features
        self.accented_words_file = os.path.join(os.path.dirname(__file__), accented_words_file)
        self.guessed_period = ''

        self.main()


    def combine_all_period_features(self):
        flattened_all_period_features = [sect for period in self.all_period_features for sect in period]
        return np.array(flattened_all_period_features)


    def guess_period(self, flattened_all_period_features):
        guess_set = []
        for m in ["MultinomialNB", "ComplementNB"]:
            filepath = os.path.join(os.path.dirname(__file__), f"models/{m}-test-model.pickle")
            with open(filepath, "rb") as f:
                model = pickle.load(f)
                guessed_period = model.predict(flattened_all_period_features)
                guess_set.append(guessed_period[0])
        self.guessed_period = guess_set[1] if guess_set[1] == "16th-Century" else guess_set[0]


    def main(self):
        self.create_accented_word_dict()
        self.get_sections_per_period()
        period_features = self.create_accented_word_feature()
        self.all_period_features.append(period_features)
        flattened_all_period_features = self.combine_all_period_features()
        self.guess_period(flattened_all_period_features)
        