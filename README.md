# Iambic Pentameter Period Classifier

## Overview
`ipclassifier` accepts a text file, which should be lines of English iambic pentameter, and outputs the period/style classification.  It only uses features derived from prosody to make a classification.


## Installation
```bash
pip install ipclassifier
```

## Usage
`ipclassifier` can be run either as a script or as a module

my_poem.txt:
```text
     All devil as I am--a damned wretch,
     A hardened, stubborn, unrepenting villain,
     Still my heart melts at human wretchedness;
     And with sincere but unavailing sighs
     I view the helpless children of distress:
     With tears indignant I behold the oppressor
     Rejoicing in the honest man's destruction,
     Whose unsubmitting heart was all his crime.--
     Ev'n you, ye hapless crew! I pity you;
     Ye, whom the seeming good think sin to pity;
     Ye poor, despised, abandoned vagabonds,
     Whom Vice, as usual, has turn'd o'er to ruin.
     Oh! but for friends and interposing Heaven,
     I had been driven forth like you forlorn,
     The most detested, worthless wretch among you!
     O injured God! Thy goodness has endow'd me
     With talents passing most of my compeers,
     Which I in just proportion have abused--
     As far surpassing other common villains
     As Thou in natural parts has given me more.

     First was the World as one great Cymbal made,
     Where Jarring Windes to infant Nature plaid.
     All Musick was a solitary sound,
     To hollow Rocks and murm'ring Fountains bound.
     Jubal first made the wilder Notes agree;
     And Jubal tun'd Musicks Jubilee:
     He call'd the Ecchoes from their sullen Cell,
     And built the Organs City where they dwell.
     Each sought a consort in that lovely place;
     And Virgin Trebles wed the manly Base.
     From whence the Progeny of numbers new
     Into harmonious Colonies withdrew.
     Some to the Lute, some to the Viol went,
     And others chose the Cornet eloquent.
     These practising the Wind, and those the Wire,
     To sing Mens Triumphs, or in Heavens quire.
     Then Musick, the Mosaique of the Air,
     Did of all these a solemn noise prepare:
     With which She gain'd the Empire of the Ear,
     Including all between the Earth and Sphear.
     Victorious sounds yet here your Homage do
     Unto a gentler Conqueror then you;
     Who though He flies the Musick of his praise,
     Would with you Heavens Hallelujahs raise.
```
NOTE: Accuracy is best with 100 or more lines.

### From the command line
```bash
python -m ipclassifier -f my_poem.txt
>>> processing starting...
>>> Your text is probably romantic
```

### As a module

my_file.py:
```python
from ipclassifier.runners import classify_ip

my_filename = "my_poem.txt"
classification = classify_ip(my_filename)
# classification = "romantic"
```

## Credit
Aside from explicit dependencies,`ipclassifier` uses code from the following projects:
- https://github.com/jrladd/regularize
- https://github.com/kylebgorman/syllabify
- https://gist.github.com/rcortini/0d05417339bc74300ce3a971442a4d3c


## Methodology
After `ipclassifier` cleans and tokenizes the input text, lines are scanned.  A set of transformations are applied until either the line can be made to conform to ideal iambic pentameter (WSWSWSWSWS) or the line is determined to be "invalid."  Here are the sequence of transformations:

1. No transformation necessary (scans as is)
2. Demote compound stresses (mostly an artifact of the initial processing--some compounds are processed as two words, with the result that a single word has two primary stresses)
3. Demote stressed monosyllables
4. Promote unstressed monosyllables
5. Promote unstressed syllables in polysyllabic words (the primary stress is not altered)
6. Demote primary stress in polysyllabic words
7. “invalid line” (if we assume that all input lines are valid, this is basically a measure of the scanner's error rate) 

For a set of lines, features are then extracted.  Here are the features:
1. A one-hot encoded array of words whose primary stress had to be altered (rule 6 above)
2. The average of the sample's transformation rules (ex: 4.2)
3. The average words per line
4. The average syllables per line
5. The individual ratios of each sample's transformation rules

These features are then fed into the model [(Complement Naive Bayes)](https://scikit-learn.org/stable/modules/generated/sklearn.naive_bayes.ComplementNB.html).

The model is trained on approximately 10,000 lines from each category (so far: Elizabethan, Victorian, Neoclassical, Romantic), using groups of 100 lines.

The trained model's accuracy is in the upper 90s.