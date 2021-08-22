import re
from string import punctuation
from pprint import pprint

from utils import args_logger
from .token import Token


class Tokenizer():
    """
    Takes in a line of IP
    Returns list of Token instances
    """

    def __init__(self, lines, dicts):
        self.lines = lines
        self.line_tokens = []
        self.remove = punctuation
        self.dicts = dicts

    def tokenize_line(self, line):
        return re.split("[ \n!\"#$%&()*+,./:;<=>?@[\]^_`{|}~  \t]", line)

    # @args_logger
    def make_initial_tokens(self):
        initial_tokens = [self.tokenize_line(line) for line in self.lines]
        # print(initial_tokens)
        return initial_tokens

    # @args_logger
    def process_lines(self):
        initial_tokens = self.make_initial_tokens()
        cleaned_tokens = [ [self.clean(token) for token in line if token not in self.remove] for line in initial_tokens]
        return cleaned_tokens

    # @args_logger
    def clean(self, word):
        word = word.lower()
        if word.endswith("'s"):
            word = word[:-2]  #+ word[-1:]
        return word

    # @args_logger
    def create_tokens(self):
        lines = self.process_lines()
        tokenized_lines = []
        for line in lines:
            tokenized_line = [Token(t, self.dicts) for t in line]
            if tokenized_line: tokenized_lines.append(tokenized_line)
        return tokenized_lines



    
