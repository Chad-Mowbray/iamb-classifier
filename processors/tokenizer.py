from nltk import word_tokenize
from string import punctuation
from utils.dicts import DictsSingleton

from utils.representer import RepresenterMixin
from utils.logger import args_logger
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s:%(message)s')

from processors.token import Token


class Tokenizer(RepresenterMixin):
    """
    Takes in a line of IP
    Returns list of Tokens
    """


    def __init__(self, lines):
        self.lines = lines
        self.line_tokens = []
        self.remove = punctuation
        self.dicts = DictsSingleton()

    @args_logger
    def make_initial_tokens(self):
        initial_tokens = [word_tokenize(line) for line in self.lines]
        return initial_tokens

    @args_logger
    def process_lines(self):
        initial_tokens = self.make_initial_tokens()
        cleaned_tokens = [ [self.clean(token) for token in line if token not in self.remove] for line in initial_tokens]
        return cleaned_tokens

    @staticmethod
    # @args_logger
    def clean(word):
        return word.lower()

    @args_logger
    def create_tokens(self):
        lines = self.process_lines()
        for line in lines:
            tokenized_line = [Token(t, self.dicts) for t in line]
            print(list(map(lambda t: print(t()), tokenized_line)))




    