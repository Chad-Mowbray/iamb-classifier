from nltk import word_tokenize
from string import punctuation
from utils.dicts import DictsSingleton

from pprint import pprint

from utils.representer import RepresenterMixin
from utils.logger import args_logger
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s:%(message)s')

from token_processors.token import Token


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

    # @args_logger
    def make_initial_tokens(self):
        initial_tokens = [word_tokenize(line) for line in self.lines]
        # print(initial_tokens)
        return initial_tokens

    # @args_logger
    def process_lines(self):
        initial_tokens = self.make_initial_tokens()
        cleaned_tokens = [ [self.clean(token) for token in line if token not in self.remove] for line in initial_tokens]
        return cleaned_tokens

    @staticmethod
    # @args_logger
    def clean(word):
        return word.lower()

    # @args_logger
    def create_tokens(self):
        lines = self.process_lines()
        # print("lines: ", lines)
        tokenized_lines = []
        for line in lines:
            # print("sentence tokens: ", [t for t in line])
            tokenized_line = [Token(t, self.dicts) for t in line]
            if tokenized_line: tokenized_lines.append(tokenized_line)
            # pprint(list(map(lambda t: print(pprint(t()), "\n"), tokenized_line)))
        # print("tokenized lines: ", tokenized_lines)
        return tokenized_lines



    