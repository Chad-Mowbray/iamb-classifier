from os.path import exists
from .feature_runner import FeatureRunner
from ipclassifier.dataprep import RawFileProcessor
from ipclassifier.classifier import Classifier

##### use local copy of nltk_data
import nltk
import os
local_path = os.path.join("".join(os.path.dirname(__file__).split('/runners')[0]),  "nltk_data")
nltk.data.path.append(local_path)



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





def get_new_list():
    import pickle
    master_changed_words = []
    files = ["c_15_master.txt", "c_16_master.txt", "c_17_master.txt", "c_18_master.txt", "c_19_rom_master.txt", "c_19_vic_master.txt"]
    for f in files:
        print("starting on ", f)
        rfp = RawFileProcessor(f"ipclassifier/runners/{f}")
        contents = rfp.cleaned_contents
        r = FeatureRunner(contents)
        changed_words = r.initial_process_contents()
        master_changed_words += changed_words

    print("done processing, starting pickling")
    with open("master_changed_words_list.pickle", "wb") as f:
        pickle.dump(master_changed_words, f)
