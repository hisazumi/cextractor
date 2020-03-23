#!/bin/sh

# generate filtered function names dictionary for each .c file
DATA_DIR=$1
TRAIN_DIR="$1/train"
TEST_DIR="$1/test"
VAL_DIR="$1/val"

TRAIN_LISTFILE="$1/copyed_train_filelist.txt"
find $TRAIN_DIR -name '*.c' > ${TRAIN_LISTFILE}

TEST_LISTFILE="$1/copyed_test_filelist.txt"
find $TEST_DIR -name '*.c' > ${TEST_LISTFILE}

VAL_LISTFILE="$1/copyed_val_filelist.txt"
find $VAL_DIR -name '*.c' > ${VAL_LISTFILE}

train_num=$(find $TRAIN_DIR -name '*.c' | wc -l)

# for train data
echo "--------------------------------------------------"
echo "make tf-idf filter for train data ..."
parallel --progress --jobs 20 'sh -c "python tfidf.py {2}/total.fdict {3} {1}.fdict > {1}.ffdict"' :::: $TRAIN_LISTFILE ::: $TRAIN_DIR ::: $train_num
echo ""

# for test data
echo "--------------------------------------------------"
echo "make tf-idf filter for test data ..."	

train_num_plus_1=$(($train_num + 1))
parallel --progress --jobs 20 'sh -c "python tfidf.py {1}.totalfdict {2} {1}.fdict > {1}.ffdict"' :::: $TEST_LISTFILE ::: $train_num_plus_1
echo ""

# for valid data
echo "--------------------------------------------------"
echo "make tf-idf filter for val data ..."
parallel --progress --jobs 20 'sh -c "python tfidf.py {1}.totalfdict {2} {1}.fdict > {1}.ffdict"' :::: $VAL_LISTFILE ::: $train_num_plus_1
echo ""


# DIR=$(find $1 -name '*.c')
# #CMD="python -W ignore tfidf.py $1/total.fdict 26417 {}.fdict > {}.ffdict"
# #parallel --jobs 20 "sh -c $CMD" ::: $DIR
# for file in $DIR; do
# 	python tfidf.py $1/total.fdict  $file.fdict > $file.ffdict
# done

