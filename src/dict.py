#!/usr/bin/python
import os
import sys
from os import listdir

try:

	f = open('../models/lm/cmu.dict')
	inp=f.readlines()
	f.close()
	dic = {} 
	for elt in inp:
		elt = elt.split('\t')
		dic[elt[0]] = 1 
	
	extension = {}
	dicts = os.listdir('../etc/' + sys.argv[1] + '/dicts')
	p = open('../etc/' + sys.argv[1] + '/tempdict','w')
	for dname in dicts:
		f = open('../etc/' + sys.argv[1] + '/dicts/'+dname)	
		inp=f.readlines()
		f.close()
		for elt in inp:
			elt = elt.split('\t');
			if elt[0] not in dic and elt[0] not in extension: 
				extension[elt[0]] = 1	
				p.write(elt[0]+"\t"+elt[1]);
	p.close();
except IOError:
	sys.exit(1);
					
	
	
