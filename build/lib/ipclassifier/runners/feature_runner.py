from collections import Counter
from ipclassifier.token_processors import Tokenizer
from ipclassifier.iambic_line_processors import IambicLine
from ipclassifier.utils import DictsSingleton



class FeatureRunner():
    """
    Coordinates input processing and feature extraction
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
        

    def initial_process_contents(self, genre=None):
        truth = []
        truth_and_lines = []
        all_changed_words = []
        all_rules = []
        all_words_per_line = []
        all_syllables_per_line = []
        tokenizer = Tokenizer(self._sentences, self._dicts)
        line_tokens: str = tokenizer.create_tokens()
        for line in line_tokens:
            iambic_line = IambicLine(line)
            changed_words = iambic_line.line_facts["changed_words"]
            all_rules.append(iambic_line.line_facts["rules_applied"])
            all_words_per_line.append(iambic_line.line_facts["words_per_line"])
            all_syllables_per_line.append(iambic_line.line_facts["syllables_per_line"])
            if changed_words: all_changed_words += changed_words
            truth.append(str(iambic_line))
            truth_and_lines.append( (str(iambic_line), [str(tkn) for tkn in line] ))
        ratios = self._get_stats(truth)
        counter_dict = Counter(all_changed_words)
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




