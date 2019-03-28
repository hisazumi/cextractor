#!/bin/sh

# generate term freqency dictionary for each .c file
DIR=$(find $1 -name '*.c')
parallel --jobs 20 'sh -c "python -W ignore cextractor.py {} -d > {}.dict"' ::: $DIR

# total document freqency for all .c.dict file
python -W ignore totaldict.py $(find $1 -name '*.c.dict') > $1/total.dict

