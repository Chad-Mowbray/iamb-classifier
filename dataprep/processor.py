import argparse
import re
from pprint import pprint

class RawFileProcessor:

    """
    

    """

    def __init__(self, filename):
        self.filename = filename
        self.raw_contents = ''
        self.cleaned_contents = []

        self.main()


    def read_file(self):
        with open(f"{self.filename}", "r") as f:
            self.raw_contents = (line for line in f.readlines())


    def print_contents(self):
        for line in self.raw_contents:
            print(line)


    def write_file(self):
        pass


    def clean_contents(self):
        cleaned = []
        for line in self.raw_contents:
            cleaned_line = line.strip()
            cleaned_line = re.sub(r'([!"#$%&\()*+,.\/:;<=>?@[\]^_{|}~\d])|(\'+$)', "", cleaned_line)
            cleaned_line = re.sub(r'(\s{2,})+|(-{2,})+', " ", cleaned_line)
            cleaned_line = re.sub(r"[\'\’]s\s{1}", " ", cleaned_line)
            cleaned.append(cleaned_line + "\n")
        self.cleaned_contents = cleaned


    def main(self):
        self.read_file()
        self.clean_contents()
        self.write_file()

        

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Input a raw iambic pentameter file to be processed')
    parser.add_argument("file")
    args = parser.parse_args()
    # print(args.file)
    rfp = RawFileProcessor(args.file)
    rfp.read_file()
    cleaned = rfp.clean_contents()
    print(cleaned)
