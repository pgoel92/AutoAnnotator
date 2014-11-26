#!/usr/bin/python
import sys

def list_decrement(ls,x):
	newls = []
	for elt in ls:
		newls.append(str(int(elt)-x));
	return newls

def list_increment(ls,x):
	newls = []
	for elt in ls:
		newls.append(str(int(elt)+x));
	return newls

try:
	f = open('../etc/' + sys.argv[1] + '/seg.txt')
	tr = f.readlines()
	words = []
	SFrm = []
	EFrm = []
	previous = 0;
	f.close();
	f = open('../etc/' + sys.argv[1] + '/decoded_timestamps','w')
	for phrase in tr:
		phrase = phrase.split();
		words = phrase[12::4]
		#print words
		SFrm = list_increment(phrase[9::4][:-1],previous)
		#print SFrm
		EFrm = list_increment(list_decrement(phrase[13::4],1),previous);
		#print EFrm
		previous = int(EFrm[-1])+1;
		#previous = 0
		#print int(EFrm[-1])+1
		for i in range(0,len(words)):
			if words[i]!="<sil>":
				#print words[i], SFrm[i], EFrm[i]
				f.write(SFrm[i]+" "+EFrm[i]+"\n");
		words = []
		SFrm = []
		EFrm = []
	f.close();
except IOError:
	sys.exit(1);
