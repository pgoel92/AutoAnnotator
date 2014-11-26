#!/bin/bash
mkdir -p ../feats/$1/fphrases
mkdir -p ../etc/$1/output/phonesegdir ../etc/$1/output/phonelabdir ../etc/$1/output/statesegdir ../etc/$1/output/aligndir 

$SPHINXBASE/bin/sphinx_fe -c ../etc/$1/fphrases -di ../twav/$1/fphrases -do ../feats/$1/fphrases -ei wav -eo mfc -mswav yes
$SPHINXDIR/bin/sphinx3_align -hmm ../models/hmm/Voxforge2 -dict ../models/lm/cmu_extended.dict -fdict ../models/lm/filler.dict -ctl ../etc/$1/fphrases.ctl -insent ../etc/$1/f.insent -cepdir ../feats/$1/fphrases -phsegdir ../etc/$1/output/phonesegdir -phlabdir ../etc/$1/output/phonelabdir -stsegdir ../etc/$1/output/statesegdir -wdsegdir ../etc/$1/output/aligndir -outsent ../etc/$1/f.outsent -hypseg ../etc/$1/fout.txt 
