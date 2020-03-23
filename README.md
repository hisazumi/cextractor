# cextractor

## Setup
cextractor requires the clang python binding.

### for Mac

install llvm
> brew install llvm

install clang binding
> pip3 install clang

and set LD_LIBRARY_PATH
> export LD_LIBRARY_PATH=/usr/local/opt/llvm/lib

## How to Use

Make dictionary

> ./dictmake.sh ../linux-4.20

Filtering terms 

> python dictfilter.py ../linux-4.20/total.dict > ../linux-4.20/filter.dict

Extract pathes

> ./extract.sh ../linux-4.20

Concatinate all pathes into one (or two or more) file

for learning
> find ../linux-4.20 -name '*.path' | xargs cat > data/linux/raw.txt

for validating
> find ../freebsd/sys/kern -name '*.path' | xargs cat > data/linux/valid.txt

for testing
> find ../freebsd/sys/i386 -name '*.path' | xargs cat > data/linux/test.txt

Preprocess extracted pathes
>  ./preprocess.sh linux

Train
> train.sh linux

Predict
predict.sh linux

Show Help

> python cextractor.py --help

Display feature for inputting code2vec

> python cextractor.py aaa.c 

Display full path for debugging

> python cextractor.py aaa.c -p 

Display AST(Abstract syntax tree) for debugging

> python cextractor.py aaa.c -a
