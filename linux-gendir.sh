#!/bin/sh

dir=$1
output=data/linux/raw/$dir.txt
rm -f $output
for file in $(find ../linux-4.20/$dir -name '*.c')
do
    python -W ignore ../cextractor/cextractor.py $file >> $output
done
