from nltk import word_tokenize

from utils.representer import RepresenterMixin
from utils.logger import args_logger
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s:%(message)s')


class Tokenizer(RepresenterMixin):
    """
    Takes in a line of IP
    Returns list of Tokens
    """


    def __init__(self, lines):
        self.lines = lines
        self.line_tokens = []

    @args_logger
    def make_initial_tokens(self):
        import inspect
        print(inspect.ismethod(self.make_initial_tokens))
        initial_tokens = [word_tokenize(line) for line in self.lines]
        return initial_tokens

    @args_logger
    def process_lines(self):
        logger.info("Tokenizer.process_lines()...")

    @args_logger
    @staticmethod
    def clean(word):
        pass



    