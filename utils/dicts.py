from nltk.corpus import words
from nltk.stem import WordNetLemmatizer
from nltk.corpus import cmudict as cmud


# words = words.words()
# lemmatizer = WordNetLemmatizer()

class DictsSingleton():
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

            cls._instance.words = words.words()
            cls._instance.lemmatizer = WordNetLemmatizer()
            cls._instance.cmudict = cmud.dict()
            
        return cls._instance

    # def __init__(self):
    #     self.words = words.words()
    #     self.lemmatizer = WordNetLemmatizer()
    #     self.cmudict = cmud.dict()

# d = DictsSingleton()
# d2 = DictsSingleton()
# print(id(d), id(d2))
