from .spelling import SpellingNormalizer



class Compounds:
    """
    If a word token cannot be found in the cmudict, checks if it is composed of two words
    should_proceed_to_compound_analysis helps reduce false positives
    """

    def __init__(self, original_word, words, lemmatizer, uk_us_dict, regularize_dicts):
        self._original_word = original_word
        self._lemmatizer = lemmatizer
        self._words = words
        self._uk_us_dict = uk_us_dict
        self.regularize_dicts = regularize_dicts


    def _should_proceed_to_compound_analysis(self):
        if self._original_word in self._words or self._original_word[:-1] in self._words:
            return False
        return True


    def find_compound_in_wordlist(self, initial=2):
        dashed_word = self._handle_dashed_word()
        if dashed_word:
            return dashed_word

        if not self._should_proceed_to_compound_analysis():
            return None

        median = len(self._original_word) // 2
        current_split_idx = 0
        wordlist = self._words
        wnl = self._lemmatizer
        res = []

        for i in range(initial, len(self._original_word) - 2):
            left = SpellingNormalizer(self._original_word[:i], self._uk_us_dict, self.regularize_dicts).modernized_word[0] or self._original_word[:i]
            right = SpellingNormalizer(wnl.lemmatize(self._original_word[i:]), self._uk_us_dict, self.regularize_dicts).modernized_word[0] or wnl.lemmatize(self._original_word[i:])
            if left in wordlist and right in wordlist:
                if current_split_idx:
                    prior_distance = abs(current_split_idx - median)
                    current_distance = abs(i - median)
                    if current_distance <= prior_distance:
                        current_split_idx = i
                        res = [self._original_word[:current_split_idx], self._original_word[current_split_idx:]]    
                else:
                    current_split_idx = i
                    res = [self._original_word[:current_split_idx], self._original_word[current_split_idx:]]
        return res or None

    
    def _handle_dashed_word(self):
        if "-" in self._original_word:
            left, right = self._original_word.split("-")[0], "".join([*self._original_word.split('-')[1:]])
            left = SpellingNormalizer(left, self._uk_us_dict, self.regularize_dicts).modernized_word[0] or left
            right = SpellingNormalizer(self._lemmatizer.lemmatize(right), self._uk_us_dict, self.regularize_dicts).modernized_word[0] or self._lemmatizer.lemmatize(right)
            if left in self._words and right in self._words:
                return [left, right]

