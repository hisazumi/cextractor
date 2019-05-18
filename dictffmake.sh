#!/bin/sh

# generate filtered function names dictionary for each .c file
DIR=$(find $1 -name '*.c')
parallel --jobs 20 'sh -c "python -W ignore tfidf.py ../linux-4.20/total.fdict 26417 {}.fdict > {}.ffdict"' ::: $DIR
