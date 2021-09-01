from os.path import exists
from .feature_runner import FeatureRunner
from ipclassifier.dataprep import RawFileProcessor
from ipclassifier.classifier import Classifier

##### use local copy on nltk_data
import nltk
import os
local_path = os.path.join("".join(os.path.dirname(__file__).split('/runners')[0]),  "nltk_data")
nltk.data.path.insert(0, local_path)



def classify_ip(filename):
    """
    Entrypoint for classifying a text file
    """

    if exists(filename):
        print("processing starting...")
        rfp = RawFileProcessor(filename)
        contents = rfp.cleaned_contents
        r = FeatureRunner(contents)
        features = r.initial_process_contents()
        c = Classifier(features)
        print(f"Your text is probably {c.guessed_period[0]}")
        return c.guessed_period[0]
    else:
        raise FileNotFoundError("Please make sure your file is in the user_input_poems/ folder.")