#/bin/bash
rm -f ../etc/$2/phrases ../etc/$2/phrases.ctl
for file in `ls ../twav/$2/phrases/*`
do
	filename=${file##*/}
	echo ${filename%.*} >> ../etc/$2/phrases
done
cp ../etc/$2/phrases ../etc/$2/phrases.ctl
mkdir -p ../feats/$2/phrases

echo "Creating MFCs from WAVs ..."
$SPHINXBASE/bin/sphinx_fe -c ../etc/$2/phrases -di ../twav/$2/phrases -do ../feats/$2/phrases -ei wav -eo mfc -mswav yes 2>../etc/$2/fe_log
echo "MFCs created successfully in the feats folder..."
$SPHINXDIR/bin/sphinx3_decode -ctl ../etc/$2/phrases.ctl -cepdir ../feats/$2/phrases -hmm ../models/hmm/Voxforge2/ -lm ../models/lm/$1.lm.dmp -dict ../models/lm/cmudict.0.7a_SPHINX_40 -fdict ../models/lm/filler.dict -hypseg ../etc/$2/seg.txt 
