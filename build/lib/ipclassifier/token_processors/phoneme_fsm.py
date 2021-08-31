from copy import deepcopy
from .spelling import SpellingNormalizer
from .compounds import Compounds
from .spelling_syllabify import SpellingSyllabifier




class PhonemeFSM():
    """
    Transforms a word token into phonemeic representation
    EX: "moon" ->  [['M', 'UW1', 'N']]
    """

    def __init__(self, token, dicts):
        self.final_phoneme_repr = []
        self.normalized_spelling = ''

        self._initial_token = token
        self._dicts = dicts 
        self._cmudict = self._dicts.cmudict
        self._uk_us_dict = self._dicts.uk_us_dict
        self._regularize_dicts = self._dicts.regularize_dicts
        self._has_apostrophe = False
        self.apostrophe_position = ''
        self._is_compound = [False, False]
        self._left_compound = ''
        self._right_compound = ''
        self._count = 0
        self._stress_assigned_diy = False

        self._lookup()


    def _check_ed(self, phonemes):
        if self._initial_token.endswith("ed") and len(self._initial_token) > 4 and not self._is_compound[0]:
            antepenult_letter = self._initial_token[-3]
            if antepenult_letter not in "aeiou":
                phonemes_copy = deepcopy(phonemes[0])
                phonemes_copy.insert(-1,'EH0')
                phonemes.append(phonemes_copy)
        return phonemes


    def _lookup(self, called_by_normalize=False, compound_token=None):
        token = self.normalized_spelling if self.normalized_spelling else self._initial_token
        token = compound_token if compound_token else token
        try:
            phonemes = self._cmudict.get(token, None)
            if phonemes is None: raise KeyError()
            phonemes = self._check_ed(phonemes)
            self._handle_success(phonemes)
        except KeyError:
            if called_by_normalize and self._count < 1:
                self._count += 1
                self._compound()
            elif called_by_normalize and self._count > 2:
                self._handle_failure()
            else:
                self._count += 1
                self._normalize(token)

    
    def _normalize(self, token):
        spelling_normalized, has_apostrophe, apostrophe_position = SpellingNormalizer(token, self._uk_us_dict, self._regularize_dicts).modernized_word
        if has_apostrophe: self._has_apostrophe = True
        if spelling_normalized: self.normalized_spelling = spelling_normalized
        if apostrophe_position: self.apostrophe_position = apostrophe_position
        if spelling_normalized:
            self._lookup(called_by_normalize=True)
        else:
            if any(self._is_compound):
                self._lookup(called_by_normalize=True)
            else:
                self._compound()
        

    def _compound(self):
        token = self.normalized_spelling if self.normalized_spelling else self._initial_token
        compound = Compounds(token, self._dicts.words, self._dicts.lemmatizer, self._uk_us_dict, self._regularize_dicts).find_compound_in_wordlist()
        if compound:
            left, right = compound[0], compound[1]
            self._is_compound[0] = True
            self._lookup(compound_token=left)
            if self._stress_assigned_diy: return
            self._is_compound[1] = True
            self._lookup(compound_token=right)
        else:
            self._handle_failure()


    def _apostrophe(self, phonemes):
        if not self._has_apostrophe: return phonemes
        if self.normalized_spelling == "the": return phonemes + [['DH']]
        if self.normalized_spelling == "to": return phonemes + [['T']]
        pop_position = 0 if self.apostrophe_position == "initial" else -1
        phonemes_copy = deepcopy(phonemes)
        reduced = []
        for word in phonemes_copy:
            filtered = [i for i,v in enumerate(word) if v[-1].isdigit()]
            word.pop(filtered[pop_position])
            reduced.append(word)
        return phonemes + reduced


    def _diy_stress_assignment(self):
        self._is_compound = [False, False]
        self._left_compound = None
        self._right_compound = None
        spelling_syllabifier = SpellingSyllabifier(self._initial_token)
        tentative_phonemes = spelling_syllabifier.tentative_phonemes
        self._stress_assigned_diy = True
        self._handle_success(tentative_phonemes)


    def _check_stress_reduction(self, phonemes):
        """
        [['K', 'AA1', 'N', 'JH', 'ER0', 'IH0', 'NG']] ->
        [['K', 'AA1', 'N', 'JH', 'ER0', 'IH0', 'NG'], ['K', 'AA1', 'N', 'JH', 'IH0', 'NG']]
        """
        if self._stress_assigned_diy: return phonemes
        new_phonemes = []
        for word in phonemes:
            for i in range(len(word) - 1):
                if word[i][-1].isdigit() and word[i+1][-1].isdigit():
                    word_copy = deepcopy(word)
                    word_copy.pop(i + 1)
                    new_phonemes.append(word_copy)
                    break
            new_phonemes.append(word)
        return new_phonemes
            

    def _handle_success(self, phonemes):
        phonemes = self._check_stress_reduction(phonemes)
        if self._stress_assigned_diy: 
            self.final_phoneme_repr = []
            if self.final_phoneme_repr:
                return
            else:
                self.final_phoneme_repr = phonemes
            return

        if any(self._is_compound):
            if self._is_compound[0]:
                self._left_compound = phonemes
                self._is_compound[0] = False
            if self._is_compound[1]:
                self._right_compound = phonemes
                self._is_compound[1] = False
        if self._left_compound and self._right_compound:
            combined = [lt + rt for lt in self._left_compound for rt in self._right_compound]
            self.final_phoneme_repr = self._apostrophe(combined)
            return

        elif self._has_apostrophe:
            reduced_phonemes = self._apostrophe(phonemes)
            self.final_phoneme_repr = reduced_phonemes
            return
        
        self.final_phoneme_repr = phonemes
        return

        
    def _handle_failure(self):
        self._diy_stress_assignment()
        return

