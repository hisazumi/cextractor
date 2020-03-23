#!/bin/sh
DATA_DIR=$1
TOTAL_FDICT=$2

DATA_LISTFILE="$1/copyed_data_filelist.txt"
find $DATA_DIR -name '*.c' > ${DATA_LISTFILE}

echo "--------------------------------------------------"
echo "make func-name dictionary for predict data ..."
parallel --progress --jobs 20 'sh -c "python -W ignore cextractor.py {} -n > {}.fdict"' :::: $DATA_LISTFILE
parallel --progress --jobs 20 'sh -c "python -W ignore test-totaldict.py {1}.fdict {2} > {1}.totalfdict"' :::: $DATA_LISTFILE ::: $TOTAL_FDICT
echo ""

# # generate term freqency dictionary for each .c file
# DIR=$(find $1 -name '*.c')
# parallel --jobs 20 'sh -c "python -W ignore cextractor.py {} -n > {}.fdict"' ::: $DIR

# parallel --jobs 20 'sh -c "python -W ignore test-totaldict.py {1}.fdict {2} > {1}.totalfdict"' ::: $DIR ::: $2

