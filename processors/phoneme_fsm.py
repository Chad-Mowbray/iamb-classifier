from utils.dicts import DictsSingleton
from processors.spelling import SpellingNormalizer
from processors.compounds import Compounds


class PhonemeFSM():

    def __init__(self, token):
        self.initial_token = token
        self.dicts = DictsSingleton()
        self.cmudict = self.dicts.cmudict
        self.current_state = "LOOKUP"
        self.is_normalized = False
        self.compound_checked = False


    def LOOKUP(self, token=None):
        token = token if token else self.initial_token
        try:
            phonemes = self.cmudict[token]
            return self.dispatch("SUCCESS", phonemes=phonemes)
        except KeyError:
            if self.is_normalized: 
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
            return self.dispatch("LOOKUP", token=spelling_normalized)

        
    def COMPOUND(self, token=None):
        token = token if token else self.initial_token
        compound = Compounds(token, self.dicts.words, self.dicts.lemmatizer).find_compound_in_wordlist()
        if compound:
            # then look up both
            left = self.dispatch("LOOKUP", token=compound[0])
            right = self.dispatch("LOOKUP", token=compound[1])
            if left and right:
                return self.dispatch("SUCCESS")
        else:
            return self.dispatch("FAILURE")


    def SUCCESS(self, phonemes=None):
        if phonemes is None: return self.final_phoneme_repr
        if hasattr(self, "final_phoneme_repr"):
            self.final_phoneme_repr[0].extend(phonemes[0])
        else:
            self.final_phoneme_repr = phonemes
        return self.final_phoneme_repr

    def FAILURE(self):
        print("FAILURE: ", self.initial_token)
        return self.initial_token


    def dispatch(self, new_state=None, **kwargs):
        # print(f"dispatch to {new_state}")
        if new_state: self.current_state = new_state
        current_method = getattr(self, self.current_state)
        return current_method(**kwargs)


        