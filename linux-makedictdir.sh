#!/bin/sh

dir=$1

if [ 0 -ne $(ls $dir/*.c | wc -l) ]
then
    for file in $(ls $dir/*.c)
    do
        python -W ignore cextractor.py $file -d > $file.dict
    done
    python -W ignore totaldict.py $dir/*.c.dict > $dir/index.dict
fi
