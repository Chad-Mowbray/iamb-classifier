from nltk.corpus import words
from nltk.stem import WordNetLemmatizer
from nltk.corpus import cmudict as cmud


class DictsSingleton():
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

            cls._instance.words = words.words()
            cls._instance.lemmatizer = WordNetLemmatizer()
            cls._instance.cmudict = cmud.dict()

            cls._instance.cmudict["us"] = [['AH1', 'S']]
            cls._instance.cmudict["heaven"] = [['HH', 'EH1', 'V', 'AH0', 'N'], ['HH', 'EH1', 'N']]
            cls._instance.cmudict["heavens"] = [['HH', 'EH1', 'V', 'AH0', 'N', 'Z'], ['HH', 'EH1', 'N', 'Z']]
            cls._instance.cmudict["heavenly"] = [['HH', 'EH1', 'V', 'AH0', 'N', 'L', 'IY0'], ['HH', 'EH1', 'N', 'L', 'IY0']]
            
        return cls._instance

