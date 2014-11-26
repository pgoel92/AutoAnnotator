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

	f = open('../etc/'+ sys.argv[1] + '/seg.txt')
	tr = f.readlines()
	f.close();
	
	words = []
	SFrm = []
	EFrm = []
	previous = 0;
	p=0
	f = open('../etc/' + sys.argv[1] + '/decoded','w')
	for phrase in tr:
		p = p+1
		phrase = phrase.split();
		words = phrase[12::4]
	#SFrm = list_increment(phrase[9::4],previous)
		EFrm = list_increment(list_decrement(phrase[13::4],1),previous);
		previous = int(EFrm[-1]) + 1;
		for i in range(0,len(words)-1):
			if words[i] != '<sil>':
				if len(words[i]) > 3:
					if words[i][-2] == '2' or words[i][-2] == '3':
						f.write(words[i][:-3]+" ");
					else:
						f.write(words[i]+" ");
				else:
						f.write(words[i]+" ");
		words = []
		SFrm = []
		EFrm = []
	f.close();

except IOError:
	sys.exit(1);
