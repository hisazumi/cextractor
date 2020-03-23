#!/bin/sh
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


# for train data
echo "--------------------------------------------------"
echo "make func-name dictionary for train data ..."
# parallel --progress --jobs 20 'sh -c "python -W ignore cextractor.py {} -n > {}.fdict"' :::: $TRAIN_LISTFILE
# python -W ignore totaldict.py $(find $TRAIN_DIR -name '*.c.fdict') > $TRAIN_DIR/total.fdict
python -W ignore totaldict.py $TRAIN_DIR > $TRAIN_DIR/total.fdict
echo ""

# for test data
echo "--------------------------------------------------"
echo "make func-name dictionary for test data ..."
parallel --progress --jobs 20 'sh -c "python -W ignore cextractor.py {} -n > {}.fdict"' :::: $TEST_LISTFILE
parallel --progress --jobs 20 'sh -c "python -W ignore test-totaldict.py {1}.fdict {2} > {1}.totalfdict"' :::: $TEST_LISTFILE ::: $TRAIN_DIR/total.fdict
echo ""

# for val data
echo "--------------------------------------------------"
echo "make func-name dictionary for val data ..."
parallel --progress --jobs 20 'sh -c "python -W ignore cextractor.py {} -n > {}.fdict"' :::: $VAL_LISTFILE
parallel --progress --jobs 20 'sh -c "python -W ignore test-totaldict.py {1}.fdict {2} > {1}.totalfdict"' :::: $VAL_LISTFILE ::: $TRAIN_DIR/total.fdict
echo ""

# # generate term freqency dictionary for each .c file
# DIR=$(find $1 -name '*.c')
# parallel --jobs 20 'sh -c "python -W ignore cextractor.py {} -n > {}.fdict"' ::: $DIR

# parallel --jobs 20 'sh -c "python -W ignore test-totaldict.py {1}.fdict {2} > {1}.totalfdict"' ::: $DIR ::: $2

