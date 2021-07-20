from nltk import sent_tokenize

from utils.representer import RepresenterMixin
from utils.logger import args_logger
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s:%(message)s')


class Sentencizer(RepresenterMixin):
    """
    Takes a text
    """
    def __init__(self, raw_text_contents):
        self.raw_text_contents = raw_text_contents
        self.text_in_lines = None

    @args_logger
    def text_to_lines(self):
        self.text_in_lines = self.raw_text_contents.split('\n')

    @args_logger
    def main(self):
        self.text_to_lines()
        # logger.debug("Sentancizer.text_in_lines: " + str(self.text_in_lines))
        return self.text_in_lines


