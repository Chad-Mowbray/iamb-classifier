from nltk.corpus import words
from nltk.stem import WordNetLemmatizer
from nltk.corpus import cmudict as cmud
from utils.uk_american import UKAmerican


class DictsSingleton():

    #C urrently ad hoc adding syllabic variation
    # TODO something better
    
    _instance = None
    def __new__(cls):

        if cls._instance is None:
            cls._instance = super().__new__(cls)

            cls._instance.words = words.words()
            cls._instance.lemmatizer = WordNetLemmatizer()
            cls._instance.cmudict = cmud.dict()
            cls._instance.uk_us_dict = UKAmerican().uk_us_dict

            cls._instance.cmudict["us"] = [['AH1', 'S']]
            cls._instance.cmudict["heaven"] = [['HH', 'EH1', 'V', 'AH0', 'N'], ['HH', 'EH1', 'N']]
            cls._instance.cmudict["heavens"] = [['HH', 'EH1', 'V', 'AH0', 'N', 'Z'], ['HH', 'EH1', 'N', 'Z']]
            cls._instance.cmudict["heavenly"] = [['HH', 'EH1', 'V', 'AH0', 'N', 'L', 'IY0'], ['HH', 'EH1', 'N', 'L', 'IY0']]
            cls._instance.cmudict["choir"] = [['K', 'W', 'AY1', 'ER0'], ['K', 'W', 'AY1', 'R']]
            cls._instance.cmudict["choirs"] = [['K', 'W', 'AY1', 'ER0', 'Z'], ['K', 'W', 'AY1', 'R', 'Z']]
            cls._instance.cmudict["forsooth"] = [[ 'F', 'ER0', 'S', 'OW1', 'TH']]
            cls._instance.cmudict["moon"] = [['M', 'UW1', 'N']]
            cls._instance.cmudict["dryad"] = [['D', 'R', "AY1", "AE0", "D"]]
            cls._instance.cmudict["dryads"] = [['D', 'R', "AY1", "AE0", "D", "Z"]]
            cls._instance.cmudict["bene"] = [['B', 'EH1', 'N', 'AH0'], ['B', 'EH1', 'N']]
            cls._instance.cmudict["wherefore"] = [["W", "EH1", "R", "F", "ER0"]]
            cls._instance.cmudict["thereon"] = [["DH", "EH0", "R", "AH1", "N"]]
            cls._instance.cmudict["whereon"] = [["W", "EH0", "R", "AH1", "N"]]
            
        return cls._instance

