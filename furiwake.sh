SOURCE_DIR="$1"

FILE_LIST_FILE="$2/filelist.txt"
SORTED_FILELIST="$2/sorted_filelist.txt"

TRAIN_FILELIST="$2/train_filelist.txt"
TEST_FILELIST="$2/test_filelist.txt"
VAL_FILELIST="$2/val_filelist.txt"

TRAIN_DIR="$2/train"
TEST_DIR="$2/test"
VAL_DIR="$2/val"

mkdir -p $2
mkdir -p $TRAIN_DIR
mkdir -p $TEST_DIR
mkdir -p $VAL_DIR

echo "get file path list"
find ${SOURCE_DIR} -name '*.c' > ${FILE_LIST_FILE}

echo "random sort"
sort -u -R --output=${SORTED_FILELIST} ${FILE_LIST_FILE}

echo "Calculating lines"
n=$(wc -l < ${SORTED_FILELIST})

n=$(echo "x=${n}; scale = 0; x / 1" | bc -l)
train_n=$(echo "x=${n} * .85; scale = 0; x / 1" | bc -l)
test_n=$(echo "x=(${n} - ${train_n}) /2; scale = 0; x / 1" | bc -l)
# val_n is the rest
train=$train_n
test=$test_n
test_top="$(( $train + 1 ))"
val="$(( $n - ( $train + $test )))"

echo "N: $n, train_n ${train}, test_n ${test} (${test_top}) , val_n ${val}"

# cat sorted_filelist.txt | { head -n ${train} > train_filelist.txt; head -n ${test} > test_filelist.txt; head -n ${val} > val_filelist.txt; }
head -n ${train} ${SORTED_FILELIST} > ${TRAIN_FILELIST}
tail -n +${test_top} ${SORTED_FILELIST} | head -n ${test} > ${TEST_FILELIST}
tail -n ${val} ${SORTED_FILELIST} > ${VAL_FILELIST}
echo "Done extracting"

echo "copy files for training..."
rm ${TRAIN_DIR}/*
count=0
while read line
do
	cp "${line}" ${TRAIN_DIR}/.
	count=$(($count + 1))
	echo -n "\r $count /$train"
done < ${TRAIN_FILELIST}
echo ""

echo "copy files for test..."
rm ${TEST_DIR}/*
count=0
while read line
do
	cp "${line}" ${TEST_DIR}/.
	count=$(($count + 1))
		echo -n "\r $count /$test"
done < ${TEST_FILELIST}
echo ""

echo "copy files for valitation..."
rm ${VAL_DIR}/*
count=0
while read line
do
	cp "${line}" ${VAL_DIR}/.
	count=$(($count + 1))	
		echo -n "\r $count /$val"
done < ${VAL_FILELIST}
echo ""

echo "N: $n, train_n ${train}, test_n ${test}, val_n ${val}"

