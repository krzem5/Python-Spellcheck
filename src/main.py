import json
import re



def read_dict(fp):
	with open(fp,"r") as f:
		return json.loads(f.read())



def correct(dct,s):
	def _repalce(m):
		def _similar(k):
			o=[]
			for i in range(0,len(k)+1):
				if (k[:i]+k[i+1:] in dct):
					o+=[k[:i]+k[i+1:]]
				if (len(k)>i+1 and k[:i]+k[i+1]+k[i]+k[i+2:] in dct):
					o+=[k[:i]+k[i+1]+k[i]+k[i+2:]]
				for c in "abcdefghijklmnopqrstuvwxyz":
					if (k[:i]+c+k[i:] in dct):
						o+=[k[:i]+c+k[i:]]
					if (k[:i]+c+k[i+1:] in dct):
						o+=[k[:i]+c+k[i+1:]]
			return o
		k=m.group(0).lower()
		if (k in dct):
			return m.group(0)
		else:
			b=k
			bp=0
			for e in _similar(k):
				if (dct[e]>bp):
					b=e
				for se in _similar(e):
					if (dct[se]>bp):
						b=se
			uc=sum([(1 if c.isupper() else 0) for c in m.group(0)])
			if (uc>=len(m.group(0))/2):
				return b.upper()
			if (m.group(0)[0].isupper()):
				return b.title()
			return b
	return re.sub(r"\w+",_repalce,s)



dct=read_dict("en.json")
print(correct(dct,"where are these Peoplse!"))
