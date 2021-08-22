import os
import pickle
from pprint import pprint
from collections import Counter

from dataprep import RawFileProcessor
from token_processors import Tokenizer
from iambic_line_processors import IambicLine
from utils import args_logger
from utils import DictsSingleton


# import nltk
# nltk.download('wordnet')



class Runner():
    """
    Main entrypoint for application
    Accepts text file
    """
    def __init__(self, sentences):
        self.sentences = sentences #Sentencizer(self.raw_file_contents).main()
        self.dicts = DictsSingleton()
        

    @staticmethod
    def _get_stats(truth):
        rules = [int(x.split(', ')[1]) for x in truth]
        total = len(rules)
        res_dict: Counter = Counter(rules)
        return {k: str(v/total * 100)[:4] + "%" for k,v in res_dict.items()}
        

    # @args_logger
    def initial_process_contents(self, genre):
        truth = []
        truth_and_lines = []
        all_changed_words = []
        tokenizer = Tokenizer(self.sentences, self.dicts)
        line_tokens: str = tokenizer.create_tokens()
        for line in line_tokens:
            iambic_line = IambicLine(line)
            changed_words = iambic_line.changed_words
            if changed_words: all_changed_words += changed_words
            truth.append(str(iambic_line))
            truth_and_lines.append( (str(iambic_line), [str(tkn) for tkn in line] ))
        pprint(truth)
        pprint([x for x in truth_and_lines if x[0][0].startswith("F")])
        total_valid_lines = len([x for x in truth if x[0].startswith("T")])
        total_lines = len(truth)
        print()
        print("Total samples: ", total_lines, "\nTotal valid lines: ", total_valid_lines, "\nsuccess rate: ", total_valid_lines / total_lines)
        ratios = self._get_stats(truth)
        print(ratios)
        print("\npercent of rule 0: ", ratios.get(0,0),"\npercent of rule 1: ", ratios.get(1,0),"\npercent of rule 2: ", ratios.get(2,0),"\npercent of rule 3: ", ratios.get(3,0), "\npercent of rule 4: ", ratios.get(4,0),"\npercent of rule 5: ", ratios.get(5,0), "\npercent failed:", ratios.get(6,0))
        print("ALL CHANGED WORDS:")
        counter_dict = Counter(all_changed_words)
        print("total changed words: ", len(counter_dict))
        # pprint(dict(counter_dict))
        # with open (f"{genre}.pickle", 'wb') as f:
        #     pickle.dump(counter_dict, f)






if __name__ == "__main__":
    # files = ["poems/elizabethan_poems.txt","poems/neoclassical_poems.txt", "poems/victorian_poems.txt","poems/romantic_poems.txt"]
    # for f in files:
    #     filename = os.path.join(os.path.dirname(__file__), f)
    #     rfp = RawFileProcessor(filename)
    #     contents = rfp.cleaned_contents

    #     r = Runner(contents)
    #     genre = f[6:16]
    #     r.initial_process_contents(genre)


    # TOTAL = Counter()
    # for file in ["elizabetha.pickle", "neoclassic.pickle", "romantic_p.pickle", "victorian_.pickle"]:
    #     with open(file, 'rb') as f:
    #         new = pickle.load(f)
    #         TOTAL += new

    # print(len(TOTAL))
    
    # with open('accented_words.txt', 'w') as f:
    #     f.writelines([word + "\n" for word in TOTAL])




    filename = os.path.join(os.path.dirname(__file__), "poems/test_poem.txt")
    rfp = RawFileProcessor(filename)
    contents = rfp.cleaned_contents
    r = Runner(contents)
    r.initial_process_contents("mixed")




    # contents = ["The leveret seat and lark and partridge nest\n"]
    # r = Runner(contents)
    # r.initial_process_contents()

    


