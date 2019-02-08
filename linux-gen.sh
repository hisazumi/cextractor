EXTCMD='python -W ignore ../cextractor/cextractor.py'

DIRS='crypto include lib scripts usr arch drivers   init     mm       security  virt block   firmware  ipc      net      sound certs   fs        kernel   samples  tools'

mkdir -p data/linux

for dir in $DIRS
do
    output=data/linux/raw/$dir.txt
    rm -f $output
    for file in `find ../linux-4.20/$dir -name '*.c'`
    do
        $EXTCMD $file >> $output
    done
done
