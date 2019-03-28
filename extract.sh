#!/bin/sh

DIR=$(find $1 -name '*.c')
# extract path for each file
parallel --jobs 20 "sh -c \"python -W ignore cextractor.py {} -f $1/filter.dict > {}.path\"" ::: $DIR

