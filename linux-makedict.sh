#!/bin/sh

FILES=`find ../linux-4.20 -name '*.c'`
for file in $FILES
do
    python -W ignore cextractor.py $file -d > $file.dict
done

