#!/bin/sh

# generate filtered function names dictionary for each .c file
DIR=$(find $1 -name '*.c')
# ~~~~~~~~~~~~~~~~~~~
CFILES_NUM=$(find $1 -name '*.c' | wc -l)

# ~~~~~~~~~~~~~~~~~~~

#CMD="python -W ignore tfidf.py $1/total.fdict 26417 {}.fdict > {}.ffdict"
#parallel --jobs 20 "sh -c $CMD" ::: $DIR
for file in $DIR; do
	python tfidf.py $1/total.fdict $CFILES_NUM $file.fdict > $file.ffdict
done

