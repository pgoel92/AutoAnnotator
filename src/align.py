#!/usr/bin/python

#Input : expected output
#	 decoded output
#	 decoded timestamps
#
#Output :
#
#	A. .lab file of the following format
#	
#		word1	start_time end_time
#		word2	start_time end_time
#		.
#		.
#		.
#		.
#		wordn	start_time end_time
#
#	 where word1,word2....wordn are words in expected output
#
#	B. falign_output file of the following format
#
#		audio_start_time#audio_end_time#text
#		.
#		.
#		.
#	 where the text is to be force aligned with audio from the 
#	 original wav file starting at audio_start_time and ending 
#	 at audio_end_time

import sys

def minimumIDS(I,D,S):
	
	if I<=D and I<=S: output = [I,2] 
	elif D<=I and D<=S: output = [D,3]
	else: output = [S,1]

	return output

def minimumSDI(I,D,S):
	
	if S<=D and S<=I: output = [S,1] 
	elif D<=I and D<=S: output = [D,3]
	else: output = [I,2]

	return output

def minimumDSI(I,D,S):
	
	if D<=S and D<=I: output = [D,3] 
	elif S<=I and S<=D: output = [S,1]
	else: output = [I,2]

	return output

def minimumISD(I,D,S):
	
	if I<=D and I<=S: output = [I,2] 
	elif S<=I and S<=D: output = [S,1]
	else: output = [D,3]

	return output
def minimumSID(I,D,S):
	
	if S<=D and S<=I: output = [S,1] 
	elif I<=D and I<=S: output = [I,2]
	else: output = [D,3]

	return output
def minimumDIS(I,D,S):
	
	if D<=I and D<=S: output = [D,3] 
	elif I<=D and I<=S: output = [I,2]
	else: output = [S,1]

	return output
def formatting(s,t):
	ls = len(s);
	lt = len(t);

	if ls == lt:
		out = [s.upper(),t.upper()]
	elif ls < lt:
		diff = lt-ls
		for i in range(0,diff):
			s = s+" "
		out = [s.upper(),t.upper()]
	else:
	  	diff = ls-lt
	  	for i in range(0,diff):
			t=t+" "
		out = [s.upper(),t.upper()]
	return out
def align(expected,decoded,decoded_time):

	r = len(expected)+1;	#No. of rows in my DP matrix
	c = len(decoded)+1;	#No. of columns in my DP matrix
	
	#Initialization
	
	DPMatrix = [] 
	PathMatrix = []

	DPMatrix = [[None for _ in range(c)] for _ in range(r)]
	PathMatrix = [[None for _ in range(c)] for _ in range(r)]

	for i in range(0,r):
		DPMatrix[i][0] = i
	for j in range(0,c):
		DPMatrix[0][j] = j

	for i in range(1,r):
		PathMatrix[i][0] = 2	#Base insertions
	for j in range(1,c):
		PathMatrix[0][j] = 3	#Base deletions

	#Alignment

	for i in range(1,r):
		for j in range(1,c):
			if expected[i-1] == decoded[j-1]:
				DPMatrix[i][j] = DPMatrix[i-1][j-1]
				PathMatrix[i][j] = 0
			else:
				mymin = minimumSDI(DPMatrix[i-1][j],DPMatrix[i][j-1],DPMatrix[i-1][j-1]);
				DPMatrix[i][j] = mymin[0]+1;
				PathMatrix[i][j] = mymin[1];
	
#	for i in range(0,r):
#		for j in range(0,c):
#			print DPMatrix[i][j],
#		print
#	print
#	for i in range(0,r):
#		for j in range(0,c):
#			print PathMatrix[i][j],
#		print

	#Optimal Path Construction
	
	i = r-1
	j = c-1
	Path = []
	insertions = 0
	deletions = 0
	subs = 0
	correct = 0
	isl_count = 0
	isl_flag = 0
	isl_begin = []
	isl_end = []

	expected_time = [None for _ in range(r)]

	threshold = 5 

	expout = []
	decout = []

	while i>0 or j>0:
		
		Path.insert(0,PathMatrix[i][j]);		
		
		if PathMatrix[i][j] == 0:			#If correct match
			
			if isl_flag == 0:		#If not in island of correct matches
							#(not an 'Island of Confidence' yet because..
							#..threshold check has not been applied) 
				endexp = i
				enddec = j
				isl_flag = 1		#Start new island
			isl_count = isl_count + 1	#Inc no. of matches in current island by 1
			
			expout.insert(0,expected[i-1]);
			decout.insert(0,decoded[j-1]);

			correct = correct + 1
			i = i-1
			j = j-1
		
		elif PathMatrix[i][j] == 1:			#If substitution

			if isl_flag == 1 and isl_count >= threshold :	#If island of confidence
				startexp = i
				startdec = j
				for k in range(0,enddec-startdec):
					expected_time[startexp+k]=decoded_time[startdec+k]		
				isl_begin.insert(0,startexp);
				isl_end.insert(0,endexp);
			isl_count = 0
			isl_flag = 0
			
			out = formatting(expected[i-1],decoded[j-1]);
			expout.insert(0,out[0]);
			decout.insert(0,out[1]);
			
			subs = subs + 1
			i = i-1
			j = j-1
		
		elif PathMatrix[i][j] == 2:
			if isl_count >= threshold and isl_flag == 1:				
				startexp = i
				startdec = j
				for k in range(0,enddec-startdec):
					expected_time[startexp+k]=decoded_time[startdec+k]		
				isl_begin.insert(0,startexp);
				isl_end.insert(0,endexp);
			isl_count = 0
			isl_flag = 0
			
			out = formatting(expected[i-1],"***");
			expout.insert(0,out[0]);
			decout.insert(0,out[1]);
			
			insertions = insertions + 1
			i = i-1
		else: 
			if isl_count >= threshold and isl_flag == 1:				
				startexp = i
				startdec = j
				for k in range(0,enddec-startdec):
					expected_time[startexp+k]=decoded_time[startdec+k]		
				isl_begin.insert(0,startexp);
				isl_end.insert(0,endexp);
			isl_count = 0
			isl_flag = 0
			
			out = formatting("***",decoded[j-1]);
			expout.insert(0,out[0]);
			decout.insert(0,out[1]);
			
			deletions = deletions + 1
			j = j-1
	
	f = open('../etc/' + sys.argv[1] + '/partial.lab','w')
	for i in range(0,r-1):
		f.write(expected[i] + " ");
		if expected_time[i]!=None:
			for elt in expected_time[i]:
				f.write(str(elt)+" ");
		 	f.write("\n");	
		else: f.write("None\n");
	f.close();

	audio_begin = 0
	audio_end = 0
	text = ""
	k = 0
	isl_exp_ind = 0		#The starting index of the island(to be force aligned) in the expected array
				#It will be used to insert timestamps into the expected array after force alignment
	f = open('../etc/' + sys.argv[1] + '/falign_input','w');
	while k < r-1:
		if expected_time[k] is None:
			if k>0: 
				audio_begin = expected_time[k-1][1] + 1 
				isl_exp_ind = k
			while k < r-1 and expected_time[k] == None:
				text = text + expected[k] + " "
				k = k+1
			audio_end = expected_time[k][0]
			f.write(str(isl_exp_ind)+"#"+str(audio_begin)+"#"+str(audio_end)+"#"+text+"\n");
			text = ""
		k = k+1
	f.close();
#	for i in range(0,len(isl_begin)):
#		for j in range(isl_begin[i],isl_end[i]):
#			print expected[j],
#		print
#	print isl_begin
#	print isl_end
#	for elt in Path:
#		print elt,
	f = open('../etc/' + sys.argv[1] + '/global_alignment','w');
	for elt in expout:
		f.write(elt + " ");
	f.write("\n");
	for elt in decout:
		f.write(elt + " ");
	f.write("\n");
	f.write("Total :" + str(len(Path)) + "\n");
	f.write("Correct :" + str(correct) + "\n");
	f.write("Insertions :" + str(insertions) + "\n");
	f.write("Deletions :" + str(deletions) + "\n");
	f.write("Substitutions :" + str(subs) + "\n");
	f.write("\n");		
	f.write("Accuracy :" + str((correct/float(len(Path)))*100));
	f.close();
	#Optimal Alignment Construction 
	
	return 1;

	
try:
	f = open('../etc/'+ sys.argv[1] +'/expected');
	inp = f.read();
	inp = inp.lower();
	expected = inp.split();
	f.close();
	
	f = open('../etc/' + sys.argv[1] + '/decoded');
	inp = f.read();
	inp = inp.lower();
	decoded = inp.split();
	f.close();
	
	f = open('../etc/' + sys.argv[1] + '/decoded_timestamps');
	inp = f.readlines();
	decoded_time = []
	for elt in inp:
		elt = elt.split();
		temp = []
		temp.append(int(elt[0]));
		temp.append(int(elt[1]));
		decoded_time.append(temp);
	
	align(expected,decoded,decoded_time);
	print "Global alignment obtained successfully!";

except (IOError, TypeError, IndexError):
	sys.exit(1);
