#!/bin/bash

function error_exit
{
	echo "$1" 1>&2
	exit 1
}
a=`cat ../etc/$2/trim_pts.txt`
rm -f ../etc/$2/twavinfo
touch ../etc/$2/twavinfo
mkdir -p ../twav/$2/phrases
#rm -f duration.txt
#touch duration.txt
prev=0
ind=1
dur_sum=0

k=0
basename=${1%.*}
for cur in $a
do
	if ! sox ../wav/$1 ../twav/$2/phrases/${basename}_phrase_$ind.wav trim $prev `echo $cur - $prev|bc`; then
		error_exit "Something wrong with sox ..."
	fi
	echo Phrase $ind [`echo $cur - $prev|bc` ] >> ../etc/$2/twavinfo
#echo $cur - $prev|bc >> duration.txt
	prev=`echo $cur|bc`
	let ind=$ind+1
done
let ind=$ind-1
echo $ind phrases created in the twav folder ...
