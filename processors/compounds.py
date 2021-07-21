
class Compounds:

    def __init__(self, original_word, words, lemmatizer):
        self.original_word = original_word
        self.lemmatizer = lemmatizer
        self.words = words



    def find_compound_in_wordlist(self, initial=2):
        median = len(self.original_word) // 2
        current_split_idx = 0
        wordlist = self.words
        wnl = self.lemmatizer
        res = []

        for i in range(initial, len(self.original_word) - 2):
            left = self.original_word[:i]
            right = wnl.lemmatize(self.original_word[i:])
            if left in wordlist and right in wordlist:
                if current_split_idx:
                    prior_distance = abs(current_split_idx - median)
                    current_distance = abs(i - median)
                    if current_distance <= prior_distance:
                        current_split_idx = i
                        res = [self.original_word[:current_split_idx], self.original_word[current_split_idx:]]    
                else:
                    current_split_idx = i
                    res = [self.original_word[:current_split_idx], self.original_word[current_split_idx:]]
        return res or None