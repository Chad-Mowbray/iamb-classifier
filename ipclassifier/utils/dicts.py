import codecs, os, json, re
from nltk.corpus import words
from nltk.stem import WordNetLemmatizer
from nltk.corpus import cmudict as cmud
from .uk_american import UKAmerican



class DictsSingleton():
    """
    Contains main reference data for looking up tokens
    Sets some ad-hoc entries
    Singleton
    """
    
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

            f = os.path.join(os.path.dirname(__file__), 'files/emspelling.json')
            with codecs.open(f, 'r', encoding='utf-8') as f:
                temp = f.read()
            g = os.path.join(os.path.dirname(__file__), 'files/decruft.json')
            with codecs.open(g, 'r', encoding='utf-8') as f:
                dec = f.read()
            decruft = json.loads(dec)
            cls._instance.regularize_dicts = {
                "decruftre_macron": {re.compile(k): v for k,v in decruft.items()},
                "decruftre": {re.compile(k): v for k,v in decruft.items() if "~" not in k},
                "dictionary": json.loads(temp)
            }
            
        return cls._instance

