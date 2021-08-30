import re
from pprint import pprint
from unidecode import unidecode


class RawFileProcessor:

    def __init__(self, src_filename):
        self.cleaned_contents = []

        self._src_filename = src_filename
        self._raw_contents = ''

        self._main()


    def read_file(self):
        with open(f"{self._src_filename}", "r") as f:
            self._raw_contents = (line for line in f.readlines())


    def print_contents(self):
        for line in self._raw_contents:
            print(line)


    def write_file(self, dest_filename):
        with open(dest_filename, 'a') as f:
            f.writelines(self.cleaned_contents)


    def clean_contents(self):
        cleaned = []
        for line in self._raw_contents:
            if len(line) < 2: continue
            cleaned_line = line.strip()
            cleaned_line = unidecode(cleaned_line)
            cleaned_line = re.sub(r'<{1}[^>]*>{1}', '', cleaned_line)
            cleaned_line = re.sub(r'([!"#$%&\()*+,.\/:;<=>?@[\]^_{|}~\d])|(\'+$)', "", cleaned_line)
            cleaned_line = re.sub(r'(\s{2,})+|(-{2,})+|(-\s+?$)', " ", cleaned_line)
            cleaned_line = re.sub(r"[\'\’]s\s{1}", " ", cleaned_line)
            cleaned_line = re.sub(r'th\'\w+', "th' ", cleaned_line)
            cleaned_line = re.sub(r'^[MXLICV]+$|CANTO.*[MXLICV]+|\[[mxlicv]+\]|^[^a-z]+$', '', cleaned_line)
            cleaned_line = re.sub(r'[æÆ]', "ae", cleaned_line)
            cleaned_line = re.sub(r'[œŒ]', "oe", cleaned_line)
            cleaned.append(cleaned_line + "\n")
        self.cleaned_contents = cleaned


    def _main(self):
        self.read_file()
        self.clean_contents()
        # self.write_file()

        

if __name__ == "__main__":
    # parser = argparse.ArgumentParser(description='Input a raw iambic pentameter file to be processed')
    # parser.add_argument("file")
    # args = parser.parse_args()
    # print(args.file)
    for filename in ["neo1.txt", "neo2.txt", "neo3.txt", "neo4.txt", "neo5.txt"]:
        rfp = RawFileProcessor(filename)
        rfp.read_file()
        rfp.clean_contents()
        rfp.write_file("neoclassical_poems.txt")