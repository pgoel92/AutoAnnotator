#!/bin/bash

function error_exit
{
	echo "$1" 1>&2
	exit 1
}
i=0
mkdir -p ../etc/$2/fdict_insent
mkdir -p ../twav/$2/fphrases
rm -f ../twav/$2/fphrases/*
rm -f ../etc/$2/f.insent ../etc/$2/findices
rm -f ../etc/$2/fdict_insent/*
echo "Creating phrases for forced alignment ..."
while read line
do
	IFS=#
	temp_array=($line)
	begin=`echo "scale=2;${temp_array[1]}/100" | bc -l`
	end=`echo "scale=2;${temp_array[2]}/100" | bc -l`
	audiolen=`echo "$end-$begin+0.01" | bc -l`
#	echo $begin $end $audiolen
	wavname=${1%.*}
	if ! sox ../wav/$1 ../twav/$2/fphrases/${wavname}_fphrase_$i.wav trim $begin $audiolen; then
		error_exit "Something wrong with sox"
	fi
	IFS=' '
	echo ${temp_array[3]} >> ../etc/$2/f.insent
	s=(${temp_array[3]})
	for word in ${s[@]}
	do
		echo $word >> ../etc/$2/fdict_insent/insent_$i
	done
	echo ${temp_array[0]} >> ../etc/$2/findices
	let i=$i+1
done < ../etc/$2/falign_input
if ! ./rename_phrases.sh ../twav/$2/fphrases; then
        error_exit "Exiting program ..."
fi

if ! ./rename_phrases.sh ../etc/$2/fdict_insent; then
        error_exit "Exiting program ..."
fi

echo $i phrases created in twav/$2/fphrases
#perl make_pronunciation.pl -tools .. -dictdir test -words ../../../Alignment/falign/insents/insent147 -dict ../../../Alignment/falign/dicts/dict147
