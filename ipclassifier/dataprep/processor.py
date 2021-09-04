import re
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
        html = re.compile(r'<{1}[^>]*>{1}')
        punctuation = re.compile(r'([!"#$%&\()*+,.\/:;<=>?@[\]^_{|}~\d])|(\'+$)')
        dashes = re.compile(r'(\s{2,})+|(-{2,})+|(-\s+?$)')
        apostrophe_s = re.compile(r"[\'\’]s\s{1}")
        the = re.compile(r'th\'\w+')
        romans = re.compile(r'^[MXLICV]+$|CANTO.*[MXLICV]+|\[[mxlicv]+\]|^[^a-z]+$')
        ae = re.compile(r'[æÆ]')
        oe = re.compile(r'[œŒ]')

        for line in self._raw_contents:
            if len(line) < 2: continue
            cleaned_line = line.strip()
            cleaned_line = unidecode(cleaned_line)
            cleaned_line = re.sub(html, '', cleaned_line)
            cleaned_line = re.sub(punctuation, "", cleaned_line)
            cleaned_line = re.sub(dashes, " ", cleaned_line)
            cleaned_line = re.sub(apostrophe_s, " ", cleaned_line)
            cleaned_line = re.sub(the, "th' ", cleaned_line)
            cleaned_line = re.sub(romans, '', cleaned_line)
            cleaned_line = re.sub(ae, "ae", cleaned_line)
            cleaned_line = re.sub(oe, "oe", cleaned_line)
            cleaned_line = re.sub("`", "'", cleaned_line)
            cleaned.append(cleaned_line + "\n")
        self.cleaned_contents = cleaned


    def _main(self):
        self.read_file()
        self.clean_contents()
        