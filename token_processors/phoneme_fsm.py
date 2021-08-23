from .spelling import SpellingNormalizer
from .compounds import Compounds
from .spelling_syllabify import SpellingSyllabifier
from copy import deepcopy


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
         #print("check_ed called")
         #print(phonemes, self._initial_token)

        if self._initial_token.endswith("ed") and len(self._initial_token) > 4 and not self._is_compound[0]:
             #print("left compound: ", self._left_compound)
             #print(self._is_compound)
             #print("\tnot a short word")
            antepenult_letter = self._initial_token[-3]
            if antepenult_letter not in "aeiou":
                phonemes_copy = deepcopy(phonemes[0])
                 #print("\t", antepenult_letter, phonemes_copy)
                phonemes_copy.insert(-1,'EH0')
                 #print("\t", phonemes_copy)
                phonemes.append(phonemes_copy)
         #print("check_ed result: ", phonemes)
        return phonemes


    def _lookup(self, called_by_normalize=False, compound_token=None):
        #  #print("compound_token: ", compound_token)
        token = self.normalized_spelling if self.normalized_spelling else self._initial_token
        token = compound_token if compound_token else token
         #print("lookup called with: ", token, len(token), self._initial_token )
        # if len(token) == 0: return []
        #  #print("token: ", token)
        try:
            phonemes = self._cmudict.get(token, None)
            #  #print("___________________________________________________", phonemes)
            if phonemes is None: raise KeyError()
            phonemes = self._check_ed(phonemes)
             #print(phonemes)
            self._handle_success(phonemes)
        except KeyError:
             #print(token ,"not found in cmudict")
            if called_by_normalize and self._count < 1:
                 #print('will call compound')
                self._count += 1
                self._compound()
            elif called_by_normalize and self._count > 2:
                 #print('will call handle failure')
                self._handle_failure()
            else:
                 #print('will call normalize')
                self._count += 1
                self._normalize(token)

    
    def _normalize(self, token):
         #print("normalize called")
        # if any(self._is_compound): self.
        spelling_normalized, has_apostrophe, apostrophe_position = SpellingNormalizer(token, self._uk_us_dict, self._regularize_dicts).modernized_word
        if has_apostrophe: self._has_apostrophe = True
        if spelling_normalized: self.normalized_spelling = spelling_normalized
        if apostrophe_position: self.apostrophe_position = apostrophe_position
        if spelling_normalized:
             #print("spelling normalized: ", spelling_normalized, "has_apostrophe:", self._has_apostrophe)
            self._lookup(called_by_normalize=True)
        else:
            if any(self._is_compound):
                self._lookup(called_by_normalize=True)
            else:
                self._compound()
        

    def _compound(self):
         #print("compound called...")
        token = self.normalized_spelling if self.normalized_spelling else self._initial_token
        compound = Compounds(token, self._dicts.words, self._dicts.lemmatizer, self._uk_us_dict, self._regularize_dicts).find_compound_in_wordlist()
        #  #print("compound: ", compound)
        if compound:
            left, right = compound[0], compound[1]
            #  #print(left, right)
             #print("left about to be checked with:", left)
            self._is_compound[0] = True
            self._lookup(compound_token=left)
             #print("left checked")
            if self._stress_assigned_diy: return

             #print("right about to be checked with:", right)
            self._is_compound[1] = True
            self._lookup(compound_token=right)
             #print("right checked")

        else:
            # self._count += 1
            # self.apostrophe()
            self._handle_failure()


    def _apostrophe(self, phonemes):
        if not self._has_apostrophe: return phonemes
         #print("apostrophe called")
         #print(phonemes, self.normalized_spelling)
        if self.normalized_spelling == "the": return phonemes + [['DH']]
        if self.normalized_spelling == "to": return phonemes + [['T']]
        pop_position = 0 if self.apostrophe_position == "initial" else -1
         #print(self.apostrophe_position)
        phonemes_copy = deepcopy(phonemes)
        reduced = []
        for word in phonemes_copy:
            filtered = [i for i,v in enumerate(word) if v[-1].isdigit()]
            word.pop(filtered[pop_position])
            reduced.append(word)
         #print(phonemes + reduced)
        return phonemes + reduced


    def _diy_stress_assignment(self):
         #print("God help you...")

        # clear out compound residue
        self._is_compound = [False, False]
        self._left_compound = None
        self._right_compound = None
        
        spelling_syllabifier = SpellingSyllabifier(self._initial_token)
        tentative_phonemes = spelling_syllabifier.tentative_phonemes
         #print("tentative_phonemes: ", tentative_phonemes)
         #print(self._is_compound, self._left_compound, self._right_compound)
        self._stress_assigned_diy = True

        self._handle_success(tentative_phonemes)


    def _check_stress_reduction(self, phonemes):
        """
        [['K', 'AA1', 'N', 'JH', 'ER0', 'IH0', 'NG']] ->
        [['K', 'AA1', 'N', 'JH', 'ER0', 'IH0', 'NG'], ['K', 'AA1', 'N', 'JH', 'IH0', 'NG']]
        """
        if self._stress_assigned_diy: return phonemes
         #print("check stress reduction called with: ", phonemes)
        new_phonemes = []
        for word in phonemes:
             #print(word)
            for i in range(len(word) - 1):
                 #print(word[i])
                if word[i][-1].isdigit() and word[i+1][-1].isdigit():
                     #print(word[i], word[i+1])
                    word_copy = deepcopy(word)
                    word_copy.pop(i + 1)
                    new_phonemes.append(word_copy)
                    break
            new_phonemes.append(word)
         #print(new_phonemes)
        return new_phonemes
            

    def _handle_success(self, phonemes):
         #print("handle_success called with: ", phonemes)
        phonemes = self._check_stress_reduction(phonemes)

        if self._stress_assigned_diy: 
             #print("handle_success stress assigned diy: ", phonemes)
             #print("handle_success stress assigned diy final_phoneme_repr before: ", self.final_phoneme_repr)
            self.final_phoneme_repr = []
            if self.final_phoneme_repr:
                return
            else:
                self.final_phoneme_repr = phonemes
             #print("handle_success stress assigned diy final_phoneme_repr after: ", self.final_phoneme_repr)
            return

        if any(self._is_compound):
             #print("checking compound: ", self._is_compound)
            if self._is_compound[0]:
                 #print("left compound: ", phonemes)
                self._left_compound = phonemes
                self._is_compound[0] = False
                #  #print("left_compound:", self._left_compound)
            if self._is_compound[1]:
                 #print("right compound: ", phonemes)
                self._right_compound = phonemes
                self._is_compound[1] = False
                #  #print("right_compound:", self._right_compound)
        if self._left_compound and self._right_compound:
             #print("both left and right are valid")
            combined = [lt + rt for lt in self._left_compound for rt in self._right_compound]
            self.final_phoneme_repr = self._apostrophe(combined)
             #print("final compound repr:!!!! ", self.final_phoneme_repr)
            return

        elif self._has_apostrophe:
            reduced_phonemes = self._apostrophe(phonemes)
            self.final_phoneme_repr = reduced_phonemes
            return
        
        self.final_phoneme_repr = phonemes
        
         #print("end of handle_success")
         #print(self.final_phoneme_repr)
        return

        
    def _handle_failure(self):
         #print("*" * 80, "Unable to parse token ", self._initial_token, "final_phoneme_repr", self.final_phoneme_repr)
        self._diy_stress_assignment()
        return

