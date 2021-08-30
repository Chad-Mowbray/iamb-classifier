import os
from os.path import exists
import pickle
from pprint import pprint
from collections import Counter
from random import shuffle

from dataprep import RawFileProcessor
from token_processors import Tokenizer
from iambic_line_processors import IambicLine
from utils import args_logger
from utils import DictsSingleton
from classifier import Classifier


# import nltk
# nltk.download('wordnet')



class Runner():
    """
    Main entrypoint for application
    Accepts text file
    """
    def __init__(self, sentences):
        self._sentences = sentences 
        self._dicts = DictsSingleton()
        

    @staticmethod
    def _get_stats(truth):
        rules = [int(x.split(', ')[1]) for x in truth]
        total = len(rules)
        res_dict: Counter = Counter(rules)
        return {k: v/total * 100 for k,v in res_dict.items()}
        

    # @args_logger
    def initial_process_contents(self, genre=None):
        truth = []
        truth_and_lines = []
        all_changed_words = []
        all_rules = []    #############################
        all_words_per_line = []
        all_syllables_per_line = []
        tokenizer = Tokenizer(self._sentences, self._dicts)
        line_tokens: str = tokenizer.create_tokens()
        for line in line_tokens:
            iambic_line = IambicLine(line)
            changed_words = iambic_line.line_facts["changed_words"]
            all_rules.append(iambic_line.line_facts["rules_applied"]) ##############
            all_words_per_line.append(iambic_line.line_facts["words_per_line"])
            all_syllables_per_line.append(iambic_line.line_facts["syllables_per_line"])
            if changed_words: all_changed_words += changed_words
            truth.append(str(iambic_line))
            truth_and_lines.append( (str(iambic_line), [str(tkn) for tkn in line] ))
        # pprint(truth)
        # pprint([x for x in truth_and_lines if x[0][0].startswith("F")])
        total_valid_lines = len([x for x in truth if x[0].startswith("T")])
        total_lines = len(truth)
        # print()
        # print("Total samples: ", total_lines, "\nTotal valid lines: ", total_valid_lines, "\nsuccess rate: ", total_valid_lines / total_lines)
        ratios = self._get_stats(truth)
        # print(ratios)
        # print("\npercent of rule 0: ", ratios.get(0,0),"\npercent of rule 1: ", ratios.get(1,0),"\npercent of rule 2: ", ratios.get(2,0),"\npercent of rule 3: ", ratios.get(3,0), "\npercent of rule 4: ", ratios.get(4,0),"\npercent of rule 5: ", ratios.get(5,0), "\npercent failed:", ratios.get(6,0))
        # print("ALL CHANGED WORDS:")
        counter_dict = Counter(all_changed_words)
        # print("total changed words: ", len(counter_dict))

        # pprint(dict(counter_dict))
        # with open (f"dataprep/pickle_jar/elizabethan/{genre}.pickle", 'wb') as f:
        #     pickle.dump(counter_dict, f)
        return {
            "counter_dict":counter_dict,
            "rules_avg": sum(all_rules) / len(all_rules),
            "words_per_line": sum(all_words_per_line) / len(all_words_per_line),
            "avg_syllables_per_line": sum([s for y in all_syllables_per_line for s in y]) / len(all_syllables_per_line),
            "rule_0": ratios.get(0,0),
            "rule_1": ratios.get(1,0),
            "rule_2": ratios.get(2,0),
            "rule_3": ratios.get(3,0),
            "rule_4": ratios.get(4,0),
            "rule_5": ratios.get(5,0),
            "rule_6": ratios.get(6,0)
        }






if __name__ == "__main__":

    if exists("classifier/models"):
        print("exists...")
        filename = "test_text.txt"
        rfp = RawFileProcessor(filename)
        contents = rfp.cleaned_contents
        r = Runner(contents)
        features = r.initial_process_contents()
        c = Classifier("accented_words.txt", features)
        print(c.guessed_period)

    else:
        print("doesn't exist")
    # check if the model exists
        # if so then read the file, process, and classify
        # else train the model










    # files = ["poems/elizabethan_poems.txt","poems/neoclassical_poems.txt", "poems/victorian_poems.txt","poems/romantic_poems.txt"]
    # for f in files:
        # filename = os.path.join(os.path.dirname(__file__), f)
        # rfp = RawFileProcessor(filename)
        # contents = rfp.cleaned_contents

        # r = Runner(contents)
        # genre = f[6:16]
        # r.initial_process_contents(genre)






    # filename = os.path.join(os.path.dirname(__file__), "poems/neoclassical_poems.txt")
    # rfp = RawFileProcessor(filename)
    # contents = rfp.cleaned_contents

    # for j in range(3):
    #     shuffle(contents)
    #     sectioned_contents = []
    #     sections = []
    #     for i,line in enumerate(contents):
    #         if i == 0: continue
    #         # print(line.rstrip("\n"))
    #         sections.append(line.rstrip("\n"))
    #         if i % 100 == 0:
    #             sectioned_contents.append(sections)
    #             sections = []
    #     # print(len(sectioned_contents))
    #     # print(len(sectioned_contents[0]))
    #     # print(len(sectioned_contents[5]))

    #     for i,section in enumerate(sectioned_contents):
    #         r = Runner(section)
    #         genre = f"neoclassical_test-{j}-{i}"
    #         r.initial_process_contents(genre)






    # TOTAL = Counter()
    # for file in ["elizabetha.pickle", "neoclassic.pickle", "romantic_p.pickle", "victorian_.pickle"]:
    #     with open(file, 'rb') as f:
    #         new = pickle.load(f)
    #         TOTAL += new

    # print(len(TOTAL))
    
    # with open('accented_words.txt', 'w') as f:
    #     f.writelines([word + "\n" for word in TOTAL])




    # filename = os.path.join(os.path.dirname(__file__), "poems/test_poem.txt")
    # rfp = RawFileProcessor(filename)
    # contents = rfp.cleaned_contents
    # r = Runner(contents)
    # r.initial_process_contents("mixed")




    # contents = ["The leveret seat and lark and partridge nest\n"]
    # r = Runner(contents)
    # r.initial_process_contents()

    


