#!/bin/bash

python dict.py $1 
cp ../models/lm/cmu.dict ../models/lm/cmu_extended.dict
cat ../etc/$1/tempdict >> ../models/lm/cmu_extended.dict
