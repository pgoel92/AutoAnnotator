#!/bin/bash

a=`ls ../twav/$1/fphrases`
rm -f ../etc/$1/fphrases
rm -f ../etc/$1/fphrases.ctl
for file in $a
do
	basename=${file%.*}
	#ind=${basename#fphrase}
	echo $basename >> ../etc/$1/fphrases
	echo $basename >> ../etc/$1/fphrases.ctl
done
