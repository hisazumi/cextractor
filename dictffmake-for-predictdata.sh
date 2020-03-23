#!/bin/sh

# generate filtered function names dictionary for each .c file
DATA_DIR=$1
TRAIN_DIR=$2

DATA_LISTFILE="$1/copyed_data_filelist.txt"
find $DATA_DIR -name '*.c' > ${DATA_LISTFILE}

train_num=$(find $TRAIN_DIR -name '*.c' | wc -l)

# for data
echo "--------------------------------------------------"
echo "make tf-idf filter for predict data ..."	

train_num_plus_1=$(($train_num + 1))
parallel --progress --jobs 20 'sh -c "python tfidf.py {1}.totalfdict {2} {1}.fdict > {1}.ffdict"' :::: $DATA_LISTFILE ::: $train_num_plus_1
echo ""


# DIR=$(find $1 -name '*.c')
# #CMD="python -W ignore tfidf.py $1/total.fdict 26417 {}.fdict > {}.ffdict"
# #parallel --jobs 20 "sh -c $CMD" ::: $DIR
# for file in $DIR; do
# 	python tfidf.py $1/total.fdict  $file.fdict > $file.ffdict
# done

