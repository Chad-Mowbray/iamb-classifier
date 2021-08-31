import csv
import os



class UKAmerican:
    """
    Creates a UK-US spelling dictionary
    """
    
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            muh_dict = cls.create_uk_us_dict()
            cls._instance.uk_us_dict = muh_dict
        return cls._instance


    @staticmethod
    def create_uk_us_dict():
        with open(os.path.join(os.path.dirname(__file__), "files/uk_american_text.txt")) as f:
            reader = csv.reader(f, delimiter="\t")
            next(reader)
            next(reader)
            return {pair[0]:pair[1] for pair in reader}
