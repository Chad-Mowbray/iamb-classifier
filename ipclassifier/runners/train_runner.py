from ipclassifier.classifier import ModelTrainer, tune_params
from .feature_runner import FeatureRunner 



def train_runner():
    ModelTrainer(FeatureRunner)

def test_params():
    tune_params()
