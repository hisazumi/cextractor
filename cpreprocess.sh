files=`find $1 -name '*.c'`
for f in $files
do
    python3 cextractor.py $f
done
