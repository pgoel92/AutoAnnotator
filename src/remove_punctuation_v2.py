#!/usr/bin/python
import sys
import re

def RemovePunctuation(s):
	Text = re.sub(r',(?=[^ ])',"",s);	#Remove all commas that are not followed by a space
	Text = re.sub(r'\.(?=[^ ])',"",Text);	#Remove all full stops that are not followed by a space
	Text = re.sub(r'[^\w\']'," ",Text);	#Replace all punctuations except apostrophe with a space
	Text = re.sub(r'(?<=\w)\'(?=\w)',"#",Text);	#Replace all apostrophes enclosed within two non-special characters with '#'
	Text = re.sub(r'\''," ",Text);		#Remove all remaining apostrophes
	Text = re.sub('#',"'",Text);		#Replace # (i.e apostrophes preserved in step 2) with apostrophe 
	Text = re.sub(r'_'," ",Text);		#Replace underscores with space
	Text = re.sub(r' +'," ",Text);		#Replace all occurrences of multiples spaces with one space
	return Text;

def RemovePunctuationExceptFullStop(s):
	#Text = re.sub(r',(?=[^ ])',"",s);	#Remove all commas that are not followed by a space
	Text = re.sub(r'\.(?=[^ ])',"",s);	#Remove all full stops that are not followed by a space
	p=re.compile(r'((?<=Mr)\.)|((?<=Mrs)\.)');
	Text = p.sub("",Text);
	Text = re.sub(r'[^\w\'\.]'," ",Text);	#Replace all punctuations except apostrophe and full stop with a space
	Text = re.sub(r'(?<=\w)\'(?=\w)',"#",Text);	#Replace all apostrophes enclosed within two non-special characters with '#'
	Text = re.sub(r'\''," ",Text);		#Remove all remaining apostrophes
	Text = re.sub('#',"'",Text);		#Replace # (i.e apostrophes preserved in step 2) with apostrophe 
	Text = re.sub(r'_'," ",Text);		#Replace underscores with space
	Text = re.sub(r' +'," ",Text);		#Replace all occurrences of multiples spaces with one space
	return Text;

def ProcessForDisplay(s):
	Text = re.sub(r',(?=[^ ])',"",s);	#Remove all commas that are not followed by a space
	Text = re.sub(r'\.(?=[^ ])',"",Text);	#Remove all full stops that are not followed by a space
	Text = re.sub(r'_|\*'," ",Text);		#Replace underscores with space
	Text = re.sub(r'\n|\r'," ",Text);		#Replace all occurrences of a single newline character with a space
	p=re.compile(r'-+(\W+)-+');
	Text = p.sub(r'\1',Text);
	Text = re.sub(r'-+'," ",Text);		#Replace all occurrences of one or more hyphens with a space
	Text = re.sub(r' +'," ",Text);		#Replace all occurrences of one or more spaces with one space
	p=re.compile(r' ([^\w ]+) ');
	#p=re.compile(r'. ([^\w ]+) .');
	Text = p.sub(r'\1 ',Text);
	#ls = p.findall(Text);
	#for item in ls: print "__" + item + "__"
	#for match in p.finditer(Text): print match.groups();
	#Text = re.sub(r'  ',"\n\n",Text);	#To preserve paragraphs, replace two continuous spaces with two newlines
						#Ideally, N spaces should be replaced with n newlines. Find out how to do that
	return Text;
	
def main():
	
	try:
		f = open("../txt/" + sys.argv[1]);
		Text = f.read();
		f.close();
	
		StrippedText = RemovePunctuation(Text);	
		StrippedTextWithFullStops = RemovePunctuationExceptFullStop(Text);
		DisplayText = ProcessForDisplay(Text);
		#a = StrippedText.split();
		b = StrippedTextWithFullStops.split('.');
		#c = DisplayText.split();
	
		f=open("../etc/" + sys.argv[2] + "/expected",'w');	
		f.write(StrippedText);
		f.close();
	
		f=open('../etc/' + sys.argv[2] + '/txt.tr','w');
		for line in b:	
			f.write("<s> " + line + " </s>\n");
		f.close();
		
		f=open('../etc/' + sys.argv[2] + '/DispText','w');
		f.write(DisplayText);
		f.close();
		#print len(a), len(b);
		#print DisplayText
	#	f = open("a",'w');
	#	for elt in a:
	#		f.write(elt+"\n");
	#	f.close();
	#	f = open("b",'w');
	#	for elt in b:
	#		f.write(elt+"\n");
	#	f.close();

	except IOError:
		sys.exit(1);

main();
