import json
import re



def read_dict(fp):
	with open(fp,"r") as f:
		return json.loads(f.read())



def correct(dct,s):
	def P(word, N=sum(dct.values())):
		"Probability of `word`."
		return dct[word] / N
	def correction(word):
		"Most probable spelling correction for word."
		return max(candidates(word), key=P)
	def candidates(word):
		"Generate possible spelling corrections for word."
		return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

	def known(words):
		"The subset of `words` that appear in the dictionary of dct."
		return set(w for w in words if w in dct)

	def edits1(word):
		"All edits that are one edit away from `word`."
		letters='abcdefghijklmnopqrstuvwxyz'
		splits=[(word[:i], word[i:]) for i in range(len(word) + 1)]
		deletes=[L + R[1:] for L, R in splits if R if L + R[1:] in dct]
		transposes=[L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1 if L + R[1] + R[0] + R[2:] in dct]
		replaces=[L + c + R[1:] for L, R in splits if R for c in letters if L + c + R[1:] in dct]
		inserts=[L + c + R for L, R in splits for c in letters if L + c + R in dct]
		return deletes + transposes + replaces + inserts

	def edits2(word):
		"All edits that are two edits away from `word`."
		return list(e2 for e1 in edits1(word) for e2 in edits1(e1))



	for k in re.findall(r"\w+",s):
		word=k.lower()
		ln=sum(dct.values())
		e=max([word]+edits1(word)+edits2(word),key=lambda k:(dct[word]/ln if word in dct else 0))
		print(f"'{k}' => '{e}'")
	return s



dct=read_dict("en.json")
print(correct(dct,"Hi!"))
