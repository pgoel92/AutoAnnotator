#!/bin/bash

partial_indices=()	#Array that stores the starting index in the required lab file of each non-aligned island
lab=()			#Array that stores the lab file. The timestamps for non-aligned islands are not yet stored
i=0
j=0
k=0

rm -f ../etc/$1/final.lab
rm -f ../etc/$1/FailedPhrases

#read the partially filled lab file
while read line
do
	lab[$j]=$line
	let j=$j+1
done < ../etc/$1/partial.lab

#read the partial indices of the non-aligned islands
while read line
do
	partial_indices[$i]=$line
	let i=$i+1
done < ../etc/$1/findices

prev=0
#read the file containing force-alignment output filenames
while read line
do
	ind=${partial_indices[k]}					#store the starting index of the current non-aligned island
	if [ $ind -ne 0 ]
	then
		prev=${lab[ind-1]##* }						#store the time elapsed upto the non-aligned island
	fi
	if ! python falign_parse_output.py $line.wdseg $1; then			#run the forced alignment output parser on current file
	echo ${line##*_} >> ../etc/$1/FailedPhrases
	fi
	if [ $? -eq 0 ]
	then
		l=0
		while read anotherline							#read the parser output for new timestamps
		do
			timesplit=($anotherline)
			let timesplit[0]=${timesplit[0]}+$prev			#add previously elapsed time to new relative timestamp
			let timesplit[1]=${timesplit[1]}+$prev
			labline=${lab[$ind+$l]%% *}		
			newlabline=`echo $labline ${timesplit[0]} ${timesplit[1]}`		 
			lab[$ind+$l]=$newlabline					#insert new timestamps into lab array	
#echo ${	lab[$ind+$l]}
			let l=$l+1
		done < ../etc/$1/falign_temporary
	fi
	let k=$k+1
done < ../etc/$1/fphrases
#echo ${lab[0]}
for item in "${lab[@]}"
do
	echo $item >> ../etc/$1/final.lab
done
rm -f ../etc/$1/falign_temporary

