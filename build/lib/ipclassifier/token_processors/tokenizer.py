import re
from string import punctuation
from .token import Token



class Tokenizer():
    """
    Takes in a line of IP
    Returns list of Token instances
    """

    def __init__(self, lines, dicts):
        self._lines = lines
        self._remove = punctuation
        self._dicts = dicts


    def _tokenize_line(self, line):
        return re.split("[ \n!\"#$%&()*+,./:;<=>?@[\]^_`{|}~  \t]", line)


    def _make_initial_tokens(self):
        initial_tokens = [self._tokenize_line(line) for line in self._lines]
        return initial_tokens


    def _process_lines(self):
        initial_tokens = self._make_initial_tokens()
        cleaned_tokens = [ [self._clean(token) for token in line if token not in self._remove] for line in initial_tokens]
        return cleaned_tokens


    def _clean(self, word):
        word = word.lower()
        if word.endswith("'s"):
            word = word[:-2]
        return word


    def create_tokens(self):
        lines = self._process_lines()
        tokenized_lines = []
        for line in lines:
            tokenized_line = [Token(t, self._dicts) for t in line]
            if tokenized_line: tokenized_lines.append(tokenized_line)
        return tokenized_lines



    
