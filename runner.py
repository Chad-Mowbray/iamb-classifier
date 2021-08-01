from token_processors.sentencizer import Sentencizer
from token_processors.tokenizer import Tokenizer
from iambic_line_processors.iambic_line import IambicLine

from utils.representer import RepresenterMixin
from utils.logger import args_logger
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s:%(message)s')



class Runner(RepresenterMixin):
    """
    Main entrypoint for application
    Accepts text file
    """
    def __init__(self, raw_file_contents):
        self.raw_file_contents = raw_file_contents
        self.sentences = Sentencizer(self.raw_file_contents).main()

    # @args_logger
    def initial_process_contents(self):
        truth = []
        tokenizer = Tokenizer(self.sentences)
        line_tokens = tokenizer.create_tokens()
        for line in line_tokens:
            iambic_line = IambicLine(line)
            truth.append(iambic_line.is_valid_pattern)
        print(truth)







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


        r = Runner(contents)
        r.initial_process_contents()

    

# disceased lamplit silver-smithes  ["disceased", "lamplit", "silver-smithes"]

# "disceased earthshattering fireflies lamp-lit gentle haunts to pass address expeditiously\n"
    # contents = "disceased to pass address the earth forsooth\n"

