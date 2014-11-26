#!/usr/bin/python
import sys

def RemovePunctuation(s,puncs):
	prev = ''
	news = ""
	for i in range(0,len(s)-1):
		if s[i] in puncs:
			if prev != ' ':			#prevent consecutive spaces
				news = news + " "
				prev = ' '
		elif s[i] == '\'':			#prevent removal of apostrophe
			if prev != ' ':
				news = news + s[i]
				prev = s[i]
		elif s[i] == ',':
			continue;
		else:
			news = news + s[i];
			prev = s[i];
	return news;

def ProcessForDisplay(s,puncs):
	prev = ''
	news = ""
	for i in range(0,len(s)-1):
		if s[i] in puncs:
			if prev != ' ':
				news = news + " "
				prev = ' '
		elif s[i] == '\'':
			if prev != ' ':
				news = news + s[i]
				prev = s[i]
		else:
			news = news + s[i];
			prev = s[i];
	return news;

def main():
	
	alphabet = [];
	lower = map(chr,range(65,91));
	upper = map(chr,range(97,123));
	for alph in lower: 
		alphabet.append(alph);
	for alph in upper:
		alphabet.append(alph);
	
	f = open("../txt/"+sys.argv[1]);
	Text = f.read();
	f.close();
	
#	PuncNotInDisplay = ['-'];
#	DispText = ProcessForDisplay(Text,PuncNotInDisplay);
#	TempDispTokens = DispText.split();
#	
#	DispTokens = [];
#	i=0;
#	while i < len(TempDispTokens)-1:
#		if len(TempDispTokens[i+1]) == 0 or (len(TempDispTokens[i+1]) == 1 and TempDispTokens[i+1] not in alphabet):
#			DispTokens.append(TempDispTokens[i] + TempDispTokens[i+1]);
#			i = i+2;
#		else: 
#			DispTokens.append(TempDispTokens[i]);
#			i = i+1;
#	
#	f = open('../etc/DisplayTokens','w');
#	for tok in DispTokens:
#		f.write(tok + "\n");
#	f.close();

	PuncNotInAlignment = ['\r','\n','\t','-','?',':',';','!',' ','"','(',')','_']
	StrippedText = RemovePunctuation(Text,PuncNotInAlignment);
	StrippedSentences = StrippedText.split('.');

	FullStop = ['.']
	StrippedText = RemovePunctuation(Text, FullStop);
	f = open('../etc/' + sys.argv[2] + '/expected','w');
	f.write(StrippedText);
	f.close();
#StrippedTokens = StrippedText.split();
	
	f = open('../etc/'+ sys.argv[2] + '/txt.tr','w');
	for Line in StrippedSentences:
		if len(Line) > 0:
			f.write("<s> " + Line + " </s>\n");
	f.close();	
	
	#if len(newsps) == len(news): print "Success";
	#else:
	#	print "Failure";
	#	print len(newsps), len(news);
	#	f = open('orig.txt','w');
	#	for item in newsps:
	#		f.write(item+"\n");
	#	f.close();
	#	f = open('punc.txt','w');
	#	for item in news:
	#		f.write(item+"\n");
	#	f.close();

main();
