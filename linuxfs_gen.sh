rm -f data/linuxfs/raw.txt
rm -f data/linuxfs/ext2.txt
rm -f data/linuxfs/ext4.txt

EXTCMD='python3.5 ../cextractor/cextractor.py'

for dir in `echo ../linux-4.20/fs/*fs`
do
    for file in `find $dir -name '*.c'`
    do
        $EXTCMD $file >> data/linuxfs/raw.txt
    done
done

for file in `find ../linux-4.20/fs/ext2 -name '*.c'`
do
    $EXTCMD $file > data/linuxfs/valid.txt
done

for file in `find ../linux-4.20/fs/ext4 -name '*.c'`
do
    $EXTCMD $file > data/linuxfs/test.txt
done

