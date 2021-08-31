# based on https://github.com/jrladd/regularize
import re



class Regularize:
    """
    Lookes yfe a wourde bene founde inn liste
    """

    def __init__(self, regularize_dicts):
        self.decruftre_macron = regularize_dicts["decruftre_macron"]
        self.decruftre = regularize_dicts["decruftre"]
        self.dictionary = regularize_dicts["dictionary"]


    def decruftify(self, word):
        poss = []
        if "~" in word or r"\u0304" in word:
            for k,v in self.decruftre_macron.items():
                if re.search(k,word) and len(poss) == 0:
                    poss.append(re.sub(k,v,word))
                elif re.search(k,word) and len(poss) != 0:
                    poss.append(re.sub(k,v,poss[-1]))
        else:
            for k,v in self.decruftre.items():
                if re.search(k,word) and len(poss) == 0:
                    poss.append(re.sub(k,v,word))
                elif re.search(k,word) and len(poss) != 0:
                    poss.append(re.sub(k,v,poss[-1]))
        if len(poss) != 0:
            return poss[-1]
        else:
            return word

    def lookup(self, word):
        word = self.decruftify(word)
        if word in self.dictionary:
            return self.dictionary[word]
        wordlower = word.lower()
        if word == word.title() and wordlower in self.dictionary:
            return self.dictionary[wordlower].title()
        if word == word.upper() and wordlower in self.dictionary:
            return self.dictionary[wordlower].upper()
        return None

    def two_word_check(self, word):
        if (word.startswith("t'") or word.startswith("th'")) and word != "th'":
            words = word.split("'")
            firstword = self.lookup(words[0]+"'") if self.lookup(words[0]+"'") is not None else ''
            secondword = self.lookup(words[1]) if self.lookup(words[1]) is not None else ''
            combined = firstword+" "+secondword
            return combined.strip()
        else:
            return self.lookup(word)

    def modernize(self, word):
        return self.two_word_check(word)
