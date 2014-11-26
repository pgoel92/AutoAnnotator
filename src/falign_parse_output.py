#!/usr/bin/python

import sys
filename=sys.argv[1]
try:
	basename='../etc/' + sys.argv[2] + '/output/aligndir/'
	f = open(basename+filename)
	inp = f.readlines()
	inp = inp[1:-1]
	f.close();
	new = []
	for elt in inp:
		elt = elt.split()
		new.append(elt)
	f = open('../etc/' + sys.argv[2] + '/falign_temporary','w')
	for elt in new:
		if elt[3] != '<s>' and elt[3] != '</s>' and elt[3] != '<sil>':
			f.write(elt[0]+" "+elt[1]+"\n")
	f.close()
except IOError:
	sys.exit(1);	
