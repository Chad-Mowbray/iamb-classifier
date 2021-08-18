from token_processors.spelling import SpellingNormalizer
from nltk.corpus import words as nltk_wordlist



class Compounds:

    def __init__(self, original_word, words, lemmatizer, uk_us_dict):
        self.original_word = original_word
        self.lemmatizer = lemmatizer
        self.words = words
        self.uk_us_dict = uk_us_dict
        # print("Compound instance created: ", self.original_word)

    def should_proceed_to_compound_analysis(self):
        if self.original_word in nltk_wordlist.words() or self.original_word[:-1] in nltk_wordlist.words():
            return False
        return True


    def find_compound_in_wordlist(self, initial=2):

        # print("find_compound_in_wordlist called")
        dashed_word = self.handle_dashed_word()
        if dashed_word:
            # print(dashed_word)
            return dashed_word

        if not self.should_proceed_to_compound_analysis():
            return None

        median = len(self.original_word) // 2
        current_split_idx = 0
        wordlist = self.words
        wnl = self.lemmatizer
        res = []

        for i in range(initial, len(self.original_word) - 2):
            left = SpellingNormalizer(self.original_word[:i], self.uk_us_dict).modernized_word[0] or self.original_word[:i]
            right = SpellingNormalizer(wnl.lemmatize(self.original_word[i:]), self.uk_us_dict).modernized_word[0] or wnl.lemmatize(self.original_word[i:])
            print("left, right in compounds: ", left, right)
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

    
    def handle_dashed_word(self):
        # print("handle_dashed_word called")
        if "-" in self.original_word:
            left, right = self.original_word.split("-")[0], "".join([*self.original_word.split('-')[1:]])
            # print("left, right in compounds, handle dashed: ", left, right)
            left = SpellingNormalizer(left, self.uk_us_dict).modernized_word[0] or left
            right = SpellingNormalizer(self.lemmatizer.lemmatize(right), self.uk_us_dict).modernized_word[0] or self.lemmatizer.lemmatize(right)
            # print(" Processed left, right in compounds, handle dashed: ", left, right)

            if left in self.words and right in self.words:
                return [left, right]

