from re import I
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
        # print(self.sentences)
        for s in self.sentences:
            tokenizer = Tokenizer(self.sentences)
            line_tokens = tokenizer.create_tokens()
            # print(" line_tokens: ",line_tokens)
            for line in line_tokens:
                # print("$$$$$$$ ", line, line_tokens)
                iambic_line_tokens = IambicLine(line)
                initial = iambic_line_tokens.initial_processing()
                # print(initial)
                is_valid_ip = iambic_line_tokens.is_valid_IP(initial)
                print(is_valid_ip)
            # break

        # print("iambic_line_tokens: ", iambic_line_tokens)
        # print(iambic_line_tokens.base_stress_pattern)
        # print("possible IP line? ", iambic_line_tokens.is_ip())






if __name__ == "__main__":
    with open("poems/test_poem.txt") as f:
        contents = f.read()
        # print(contents)
        # print(type(contents))

        # contents = "disceased to pass address the earth aspect\n"  
        # contents = "the expeditious pass address within\n"  
        # contents = "abbreviated"
        # contents = "disceased to pass address the earth respect\n"  
        # contents = "disceased to pass address the earth aspect\nthe expeditious pass address within\ndisceased to pass address the earth respect\n" 
        # contents = "But we have left those gentle haunts to pass\n"

        r = Runner(contents)
        r.initial_process_contents()

    

# disceased lamplit silver-smithes  ["disceased", "lamplit", "silver-smithes"]

# "disceased earthshattering fireflies lamp-lit gentle haunts to pass address expeditiously\n"
    # contents = "disceased to pass address the earth forsooth\n"

