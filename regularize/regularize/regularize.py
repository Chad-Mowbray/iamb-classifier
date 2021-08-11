# #! /usr/bin/env python

# import sys, codecs, os, json, re

# f = os.path.join(os.path.dirname(__file__), 'emspelling.json')
# temp = codecs.open(f, 'r', encoding='utf-8').read()

# dictionary = json.loads(temp)

# g = os.path.join(os.path.dirname(__file__), 'decruft.json')
# dec = codecs.open(g, 'r', encoding='utf-8').read()

# decruft = json.loads(dec)
# decruftre_macron = {re.compile(k): v for k,v in decruft.items()}
# decruftre = {re.compile(k): v for k,v in decruft.items() if "~" not in k}

# def decruftify(word):
# 	poss = []
# 	if "~" in word or r"\u0304" in word:
# 		for k,v in decruftre_macron.items():
# 			if re.search(k,word) and len(poss) == 0:
# 				poss.append(re.sub(k,v,word))
# 			elif re.search(k,word) and len(poss) != 0:
# 				poss.append(re.sub(k,v,poss[-1]))
# 	else:
# 		for k,v in decruftre.items():
# 			if re.search(k,word) and len(poss) == 0:
# 				poss.append(re.sub(k,v,word))
# 			elif re.search(k,word) and len(poss) != 0:
# 				poss.append(re.sub(k,v,poss[-1]))
# 	if len(poss) != 0:
# 		return poss[-1]
# 	else:
# 		return word

# def lookup(word):

# 	word = decruftify(word)
# 	if word in dictionary:
# 		return dictionary[word]
# 	wordlower = word.lower()
# 	if word == word.title() and wordlower in dictionary:
# 		return dictionary[wordlower].title()
# 	if word == word.upper() and wordlower in dictionary:
# 		return dictionary[wordlower].upper()
# 	return None

# def two_word_check(word):
# 	if word.startswith("t'") or word.startswith("th'"):
# 		words = word.split("'")
# 		firstword = lookup(words[0]+"'")
# 		secondword = lookup(words[1])
# 		return firstword+" "+secondword
# 	else:
# 		return lookup(word)

# def modernize(text):
# 	if " " in text:
# 		wordlist = re.split('([\n\r",.?!:;\-\(\)\s+])', text)
# 		newlist = [two_word_check(word) for word in wordlist]
# 		newtext = ''.join(newlist)
# 		return newtext
# 	else:
# 		return two_word_check(text)


import sys, codecs, os, json, re

f = os.path.join(os.path.dirname(__file__), 'emspelling.json')
temp = codecs.open(f, 'r', encoding='utf-8').read()

dictionary = json.loads(temp)

g = os.path.join(os.path.dirname(__file__), 'decruft.json')
dec = codecs.open(g, 'r', encoding='utf-8').read()

decruft = json.loads(dec)
decruftre_macron = {re.compile(k): v for k,v in decruft.items()}
decruftre = {re.compile(k): v for k,v in decruft.items() if "~" not in k}

def decruftify(word):
	print(word)
	poss = []
	if "~" in word or r"\u0304" in word:
		for k,v in decruftre_macron.items():
			if re.search(k,word) and len(poss) == 0:
				poss.append(re.sub(k,v,word))
			elif re.search(k,word) and len(poss) != 0:
				poss.append(re.sub(k,v,poss[-1]))
	else:
		for k,v in decruftre.items():
			# print(k,v)
			if re.search(k,word) and len(poss) == 0:
				poss.append(re.sub(k,v,word))
			elif re.search(k,word) and len(poss) != 0:
				poss.append(re.sub(k,v,poss[-1]))
	if len(poss) != 0:
		return poss[-1]
	else:
		return word

def lookup(word):
	print("###### lookup",word )

	word = decruftify(word)
	if word in dictionary:
		return dictionary[word]
	wordlower = word.lower()
	if word == word.title() and wordlower in dictionary:
		return dictionary[wordlower].title()
	if word == word.upper() and wordlower in dictionary:
		return dictionary[wordlower].upper()
	return None

def two_word_check(word):
	print("###### two word check",word )
	if word.startswith("t'") or word.startswith("th'") and word != "th'":

		words = word.split("'")
		firstword = lookup(words[0]+"'")
		secondword = lookup(words[1])
		return firstword+" "+secondword
	else:
		return lookup(word)

def modernize(text):
	print("#### modernize called with", text)
	if " " in text:
		wordlist = re.split('([\n\r",.?!:;\-\(\)\s+])', text)
		newlist = [two_word_check(word) for word in wordlist]
		newtext = ''.join(newlist)
		return newtext
	else:
		return two_word_check(text)


if __name__ == "__main__":
    w = lookup("th'")
    print(w)