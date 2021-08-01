from token_processors.spelling import SpellingNormalizer


class Compounds:

    def __init__(self, original_word, words, lemmatizer):
        self.original_word = original_word
        self.lemmatizer = lemmatizer
        self.words = words

    def find_compound_in_wordlist(self, initial=2):

        # print("find_compound_in_wordlist called")
        dashed_word = self.handle_dashed_word()
        if dashed_word:
            # print(dashed_word)
            return dashed_word


        median = len(self.original_word) // 2
        current_split_idx = 0
        wordlist = self.words
        wnl = self.lemmatizer
        res = []

        for i in range(initial, len(self.original_word) - 2):
            left = SpellingNormalizer(self.original_word[:i]).modernized_word or self.original_word[:i]
            right = SpellingNormalizer(wnl.lemmatize(self.original_word[i:])).modernized_word or wnl.lemmatize(self.original_word[i:])
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
            left, right = self.original_word.split("-")
            left = SpellingNormalizer(left).modernized_word or left
            right = SpellingNormalizer(self.lemmatizer.lemmatize(right)).modernized_word or self.lemmatizer.lemmatize(right)
            if left in self.words and right in self.words:
                return [left, right]

