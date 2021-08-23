# from https://github.com/jrladd/regularize
import sys, codecs, os, json, re


# f = os.path.join(os.path.dirname(__file__), 'emspelling.json')
# temp = codecs.open(f, 'r', encoding='utf-8').read()

# dictionary = json.loads(temp)

# g = os.path.join(os.path.dirname(__file__), 'decruft.json')
# dec = codecs.open(g, 'r', encoding='utf-8').read()

# decruft = json.loads(dec)
# decruftre_macron = {re.compile(k): v for k,v in decruft.items()}
# decruftre = {re.compile(k): v for k,v in decruft.items() if "~" not in k}

class Regularize:
    def __init__(self, regularize_dicts):
        self.decruftre_macron = regularize_dicts["decruftre_macron"]
        self.decruftre = regularize_dicts["decruftre"]
        self.dictionary = regularize_dicts["dictionary"]
        # word = word


    def decruftify(self, word):
        #print(word)
        poss = []
        if "~" in word or r"\u0304" in word:
            for k,v in self.decruftre_macron.items():
                if re.search(k,word) and len(poss) == 0:
                    poss.append(re.sub(k,v,word))
                elif re.search(k,word) and len(poss) != 0:
                    poss.append(re.sub(k,v,poss[-1]))
        else:
            for k,v in self.decruftre.items():
                #  #print(k,v)
                if re.search(k,word) and len(poss) == 0:
                    poss.append(re.sub(k,v,word))
                elif re.search(k,word) and len(poss) != 0:
                    poss.append(re.sub(k,v,poss[-1]))
        if len(poss) != 0:
            return poss[-1]
        else:
            return word

    def lookup(self, word):
        #print("###### lookup",word, type(word) )
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
        #print("###### two word check",word )
        if (word.startswith("t'") or word.startswith("th'")) and word != "th'":
            #print("...the...")
            words = word.split("'")
            firstword = self.lookup(words[0]+"'") if self.lookup(words[0]+"'") is not None else ''
            secondword = self.lookup(words[1]) if self.lookup(words[1]) is not None else ''
            #print(firstword, secondword)
            combined = firstword+" "+secondword
            return combined.strip()
        else:
            return self.lookup(word)

    def modernize(self, word):
        #print("#### modernize called with", text)
        return self.two_word_check(word)



# if __name__ == "__main__":
#     w = lookup("th'")
     #print(w)