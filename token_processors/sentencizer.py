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
        # print("Sentencizer instance created: ", self.raw_text_contents)

    # @args_logger
    def text_to_lines(self):
        self.text_in_lines = [l for l in self.raw_text_contents.split('\n') if l]

    # @args_logger
    def main(self):
        self.text_to_lines()
        # logger.debug("Sentancizer.text_in_lines: " + str(self.text_in_lines))
        # print("Sentencizer text in lines: ", self.text_in_lines)
        return self.text_in_lines


