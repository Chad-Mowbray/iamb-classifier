from processors.sentancizer import Sentancizer
from processors.tokenizer import Tokenizer

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
        logging.info("Runner init...")
        self.raw_file_contents = raw_file_contents

    @args_logger
    def initial_process_contents(self):
        logging.info("Runner.initial_process_contents...")
        s = Sentancizer(self.raw_file_contents)
        lines = s.main()
        t = Tokenizer(lines)
        t.make_initial_tokens()







if __name__ == "__main__":
    with open("poems/test_poem.txt") as f:
        contents = f.read()
        r = Runner(contents)
        r.initial_process_contents()

