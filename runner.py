import os

from dataprep.processor import RawFileProcessor
from token_processors.sentencizer import Sentencizer
from token_processors.tokenizer import Tokenizer
from iambic_line_processors.iambic_line import IambicLine

from pprint import pprint

from utils.representer import RepresenterMixin
from utils.logger import args_logger
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s:%(message)s')

# import nltk
# nltk.download('wordnet')
from collections import Counter


class Runner(RepresenterMixin):
    """
    Main entrypoint for application
    Accepts text file
    """
    def __init__(self, sentences):
        # self.raw_file_contents = raw_file_contents
        self.sentences = sentences #Sentencizer(self.raw_file_contents).main()
        print(self.sentences)

    @staticmethod
    def get_stats(truth):
        rules = [int(x.split(', ')[1]) for x in truth]
        total = len(rules)
        res_dict = Counter(rules)
        return {k: str(v/total * 100)[:4] + "%" for k,v in res_dict.items()}
        

    # @args_logger
    def initial_process_contents(self):
        truth = []
        truth_and_lines = []
        tokenizer = Tokenizer(self.sentences)
        line_tokens = tokenizer.create_tokens()
        for line in line_tokens:
            iambic_line = IambicLine(line)
            truth.append(str(iambic_line))
            truth_and_lines.append( (str(iambic_line), [str(tkn) for tkn in line] ))
        print("xzyabcd")
        pprint(truth)
        pprint([x for x in truth_and_lines if x[0][0].startswith("F")])
        total_valid_lines = len([x for x in truth if x[0].startswith("T")])
        total_lines = len(truth)
        print()
        print("Total samples: ", total_lines, "\nTotal valid lines: ", total_valid_lines, "\nsuccess rate: ", total_valid_lines / total_lines)
        ratios = self.get_stats(truth)
        print(ratios)
        print("\npercent of rule 0: ", ratios.get(0,0),"\npercent of rule 1: ", ratios.get(1,0),"\npercent of rule 2: ", ratios.get(2,0),"\npercent of rule 3: ", ratios.get(3,0), "\npercent of rule 4: ", ratios.get(4,0),"\npercent of rule 5: ", ratios.get(5,0), "\npercent failed:", ratios.get(6,0))






if __name__ == "__main__":
    # files = ["poems/elizabethan_poems.txt","poems/neoclassical_poems.txt", "poems/victorian_poems.txt","poems/romantic_poems.txt"]
    # for f in files:
    #     filename = os.path.join(os.path.dirname(__file__), f)
    #     rfp = RawFileProcessor(filename)
    #     contents = rfp.cleaned_contents

    #     r = Runner(contents)
    #     r.initial_process_contents()



    contents = ["The leveret seat and lark and partridge nest\n"]
    r = Runner(contents)
    r.initial_process_contents()

    


