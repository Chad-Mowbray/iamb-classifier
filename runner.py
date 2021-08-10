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
    def __init__(self, raw_file_contents):
        self.raw_file_contents = raw_file_contents
        self.sentences = Sentencizer(self.raw_file_contents).main()

    @staticmethod
    def get_stats(truth):
        rules = [int(x.split(', ')[1]) for x in truth]
        total = len(rules)
        res_dict = Counter(rules)
        return {k: str(v/total * 100)[:4] + "%" for k,v in res_dict.items()}
        

    # @args_logger
    def initial_process_contents(self):
        truth = []
        tokenizer = Tokenizer(self.sentences)
        line_tokens = tokenizer.create_tokens()
        for line in line_tokens:
            iambic_line = IambicLine(line)
            truth.append(str(iambic_line))
        pprint(truth)
        total_valid_lines = len([x for x in truth if x[0].startswith("T")])
        total_lines = len(truth)
        print()
        print("Total samples: ", total_lines, "\nTotal valid lines: ", total_valid_lines, "\nsuccess rate: ", total_valid_lines / total_lines)
        ratios = self.get_stats(truth)
        print(ratios)
        print("\npercent of rule 0: ", ratios.get(0,0),"\npercent of rule 1: ", ratios.get(1,0),"\npercent of rule 2: ", ratios.get(2,0),"\npercent of rule 3: ", ratios.get(3,0), "\npercent of rule 4: ", ratios.get(4,0),"\npercent of rule 5: ", ratios.get(5,0), "\npercent failed:", ratios.get(6,0))






if __name__ == "__main__":
    with open("poems/test_poem.txt") as f:
        contents = f.read()
        # print(contents)
        # print(type(contents))

        # contents = "disceased to pass address the earth aspect\n"  
        # contents = "the expeditious pass address within\n"  
        # contents = "abbreviated once for this I strike"
        # contents = "disceased to pass address the earth respect\n"  
        # contents = "disceased to pass address the earth aspect\nthe expeditious pass address within\ndisceased to pass address the earth respect\n" 
        # contents = "But we have left those gentle haunts to pass\n"
        # contents = "Sees his own face, self-slain Humanity,\n"
        # contents = "humanity itself the race to pass"
        # contents = "the lamp-sun lamps beyond the earth respect\n"
        # contents = "Lamp lit his face, moon-river hit his side\n"
        # contents = "Both must alike from Heav'n derive their light,\nBoth must alike from Heaven derive their light,\nBoth must alike from Heav'n derive their light,\nBoth must alike from Heaven derive their light,\n"
        # contents = "Both must alike from Heaven derive their light,\nBoth must alike from Heav'n derive their light,\n"
        # contents = "Both deregulatory Heav'n their light,"

        # contents = "silver-smithes"
        # contents = "Of Oreb, or of Sinai, didst inspire"
        # contents = "moonfaced"
        # contents= "And see thy blood warm when thou feel'st it cold."
        # contents = "Where Goneril's soul made chill and foul the mist,"
# 

        r = Runner(contents)
        r.initial_process_contents()

    

# disceased lamplit silver-smithes  ["disceased", "lamplit", "silver-smithes"]

# "disceased earthshattering fireflies lamp-lit gentle haunts to pass address expeditiously\n"
    # contents = "disceased to pass address the earth forsooth\n"

