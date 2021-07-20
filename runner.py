from processors.sentencizer import Sentencizer
from processors.tokenizer import Tokenizer

from utils.representer import RepresenterMixin
from utils.logger import args_logger
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s:%(message)s')

from nltk.corpus import cmudict as cmud

cmudict = cmud.dict()


class Runner(RepresenterMixin):
    """
    Main entrypoint for application
    Accepts text file
    """
    def __init__(self, raw_file_contents):
        self.raw_file_contents = raw_file_contents

    @args_logger
    def initial_process_contents(self):
        sentencizer = Sentencizer(self.raw_file_contents)
        lines = sentencizer.main()
        tokenizer = Tokenizer(lines, cmudict)
        tokenizer.create_tokens()




if __name__ == "__main__":
    with open("poems/test_poem.txt") as f:
        contents = f.read()
        contents = " sssdkjsdh347shjdksjhds lamp-lit gentle haunts to pass address expeditiously\n"
        r = Runner(contents)
        r.initial_process_contents()

