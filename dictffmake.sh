#!/bin/sh

# generate filtered function names dictionary for each .c file
DIR=$(find $1 -name '*.c')
CMD="python -W ignore tfidf.py $1/total.fdict 26417 {}.fdict > {}.ffdict"

parallel --jobs 20 "sh -c $CMD" ::: $DIR
