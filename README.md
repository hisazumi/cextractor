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

Show Help

> python cextractor.py --help

Display feature for inputting code2vec

> python cextractor.py aaa.c 

Display full path for debugging

> python cextractor.py aaa.c -p 

Display AST(Abstract syntax tree) for debugging

> python cextractor.py aaa.c -a
