#!/bin/bash
# $1 : Big text file
# $2 : Big WAV file

function error_exit
{
	echo "$1" 1>>$2/err.log
}

txts=()
wavs=()

curdir=`pwd`
scriptdir=${0%/*}

rm -f err.log

k=0
for txt in `cat $1`
do
	txts[k]=$txt
	let k=$k+1
done

k=0
for wav in `cat $2`
do
	wavs[k]=$wav
	let k=$k+1
done

#if ! cp ${txts[i]} $scriptdir/../txt; then
#	error_exit "Error copying text file! Exiting program ..."
#fi
#if ! cp ${wavs[i]} $scriptdir/../wav; then
#	error_exit "Error copying WAV file! Exiting program ..."
#fi

if ! cd $scriptdir; then
	error_exit "Could not change directory! Exiting program ..."
fi

i=0

while [ $i -lt $k ]
do

txtfilename=${txts[i]}
wavfilename=${wavs[i]}

foldername=${txtfilename%.*}

#echo $txtfilename $wavfilename $foldername
#
#
#
mkdir -p ../etc/$foldername

echo "Obtaining break points at silence regions in the WAV file ..."
if ! python silence_detection.py $wavfilename $foldername; then
	error_exit "Exiting program ..."
fi
	
echo "Breaking WAV file into phrases ..."
if ! ./create_phrases.sh $wavfilename $foldername; then
	error_exit "Exiting program ..."
fi
if ! ./rename_phrases.sh ../twav/$foldername/phrases; then
	error_exit "Exiting program ..."
fi

echo "Preprocessing text file ..."
if ! python remove_punctuation_v2.py $txtfilename $foldername; then
	error_exit "$foldername failed at remove_punctuation_v2.py ..." $curdir
fi
echo "Creating language model from text ..."
if ! ./create_lm.sh $txtfilename $foldername; then
	error_exit "$foldername failed at create_lm.sh ..." $curdir
fi

if ! ./asr.sh $txtfilename $foldername; then
	error_exit "Exiting program ..."
fi
if ! python get_asr_output.py $foldername; then
	error_exit "$foldername failed at get_asr_output.py ..." $curdir
fi
if ! python get_asr_timestamps.py $foldername; then
	error_exit "$foldername failed at get_asr_timestamps.py ..." $curdir
fi

#echo "Aligning decoded text with expected text ..."
#if ! python align.py $foldername; then
#	error_exit "$foldername failed at align.py ..." $curdir
#fi
# 
#if ! ./falign_inputgen.sh $wavfilename $foldername; then
#	error_exit "$foldername failed at falign_inputgen.sh ..." $curdir
#fi
#
#if ! ./falign_makedict.sh $foldername; then
#	error_exit "$foldername failed at falign_makedict.sh ..." $curdir
#fi
#
#if ! ./falign_setup.sh $foldername; then
#	error_exit "$foldername failed at falign_setup.sh ..." $curdir
#fi
#
#if ! ./falign_augmentdic.sh $foldername; then
#	error_exit "$foldername failed at falign_augmentdic.sh ..." $curdir
#fi
#
#if ! ./falign.sh $foldername; then
#	error_exit "$foldername failed at falign.sh ..." $curdir
#fi
#
#if ! ./falign_addtime.sh $foldername; then
#	error_exit "$foldername failed at falign_addtime.sh ..." $curdir
#fi
#let i=$i+1
#done

cd $curdir
