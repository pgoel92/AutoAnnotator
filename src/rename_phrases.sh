#!/bin/bash
curdir=`pwd`
cd $1 
extensions=()
indices=()
prefixes=()
k=0
max_len=0

#basename=${1%.*}
#for a in ${basename}_$3_[0-9]* 
for a in `ls *`
do
	if [ `expr index $a .` -eq 0 ]
	then
	ext=''
	else
	ext=.${a##*.}		#Store file extension
	fi
	extensions[k]=$ext
	b=${a%.*}		#Remove file extension
	prefix=${b%_*}_	#Store filename prefix
	prefixes[k]=$prefix
	c=${b##*_}		#Store index
	indices[k]=$c
	#echo $prefix $c $ext
	let k=$k+1
	if [ ${#c} -gt $max_len ]
	then
	let max_len=${#c}
	fi
#mv $a `printf phrase%02d.wav ${b#phrase}`
done

j=0
while [ $j -lt $k ]
do
	if [ ${#indices[j]} -lt $max_len ]
	then
		#mv phrase$n.wav `printf phrase%.${max_len}d.wav"\n" $n `
		mv ${prefixes[j]}${indices[j]}${extensions[j]} `printf ${prefixes[j]}%.${max_len}d${extensions[j]}"\n" ${indices[j]} `
		#printf ${prefixes[j]}%.${max_len}d.${extensions[j]}"\n" ${indices[j]} 
	fi
	let j=$j+1
done
cd $curdir 
