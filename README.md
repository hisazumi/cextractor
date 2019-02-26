# cextractor

## Setup
cextractor requires the clang python binding.

Install the binding according to instructions such as:
Mac: http://asdm.hatenablog.com/entry/2015/01/08/170707

## How to Use

Show Help

> python cextractor.py --help

Display feature for inputting code2vec

> python cextractor.py aaa.c 

Display full path for debugging

> python cextractor.py aaa.c -p 

Display AST(Abstract syntax tree) for debugging

> python cextractor.py aaa.c -a
