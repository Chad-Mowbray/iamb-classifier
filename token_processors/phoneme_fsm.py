from utils.dicts import DictsSingleton
from token_processors.spelling import SpellingNormalizer
from token_processors.compounds import Compounds


class PhonemeFSM():

    def __init__(self, token):
        self.initial_token = token
        self.dicts = DictsSingleton()
        self.cmudict = self.dicts.cmudict
        self.current_state = "LOOKUP"
        self.is_normalized = False
        self.compound_checked = False
        self.spelling_normalized = ''

    def __str__(self):
        return f"""
        initial: {self.initial_token}
        state: {self.current_state}
        is_normalized: {self.is_normalized}
        compound_checked: {self.compound_checked}
        spelling_normalized: {self.spelling_normalized}
        """


    def LOOKUP(self, token=None):
        token = token if token else self.initial_token
        try:
            phonemes = self.cmudict[token]
            return self.dispatch("SUCCESS", phonemes=phonemes)
        except KeyError:
            if self.is_normalized or self.compound_checked: 
                if self.compound_checked:
                    return self.dispatch("FAILURE")
                return self.dispatch("COMPOUND", token=token)
            return self.dispatch("NORMALIZE")


    def NORMALIZE(self):
        spelling_normalized = SpellingNormalizer(self.initial_token).modernized_word
        if spelling_normalized is None:
            return self.dispatch("COMPOUND")
        else:
            self.is_normalized = True
            # print("normalized: ", spelling_normalized)
            self.spelling_normalized = spelling_normalized
            return self.dispatch("LOOKUP", token=spelling_normalized)

        
    def COMPOUND(self, token=None):
        token = token if token else self.initial_token
        compound = Compounds(token, self.dicts.words, self.dicts.lemmatizer).find_compound_in_wordlist()
        # print("compounds: ", compound)
        self.compound_checked = True
        if compound:
            # then look up both
            left = self.dispatch("LOOKUP", token=compound[0])
            right = self.dispatch("LOOKUP", token=compound[1])
            # print("Right: ", right, "left", left, "compound: ", compound)
            if left[0] and right[0]:
                # print('Both left and right:', left, right)
                return self.dispatch("SUCCESS")
        return self.dispatch("FAILURE")


    def SUCCESS(self, phonemes=None):
        # print("SUCCESS called")
        if phonemes is None: 
            # print("SUCCESS called, phonemes None")
            return self.final_phoneme_repr
        if hasattr(self, "final_phoneme_repr"):
            self.final_phoneme_repr[0].extend(phonemes[0])
            # print("SUCCESS called, has final_phoneme_repr: ", self.final_phoneme_repr, "phonemes: ", phonemes)
        else:
            # print("SUCCESS first: phonemes: ", phonemes)
            self.final_phoneme_repr = phonemes

        # print("SUCCESS called, returning final_phoneme_repr")
        return self.final_phoneme_repr

    def FAILURE(self):
        # print("FAILURE: ", self.initial_token)
        self.final_phoneme_repr = [[]]
        self.current_state = "FAILURE"
        return self.final_phoneme_repr


    def dispatch(self, new_state=None, **kwargs):
        # print(f"dispatch to {new_state}")
        if new_state: self.current_state = new_state
        current_method = getattr(self, self.current_state)
        return current_method(**kwargs)


        