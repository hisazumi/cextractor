 <!-- -*- coding: utf-8 -*- -->

# cextractor

## Setup
cextractor requires the clang python binding.

### for Mac

【install llvm】  
brew install llvm  
> llvm(コンパイラのバックエンド)をインストール。

【install clang binding】

pip3 install clang

> clang(コンパイラのフロントエンド)をインストール。読み方はクラン。


 【and set LD_LIBRARY_PATH】

export LD_LIBRARY_PATH=/usr/local/opt/llvm/lib

> パスの設定。ライブラリの場所をlibに指定。


## How to Use

Login

> ssh dl-box.local
> dl-box.localにssh接続。

Directrory

> /data2/c2v/cextractor
> cextractorまで行く。

Make dictionary

> ./dictmake.sh ../linux-4.20
> 一つ前に戻ってlinux-4.20に./dictmake.shの結果を出力 ここに辞書を作る。

Filtering terms 

> python dictfilter.py ../linux-4.20/total.dict > ../linux-4.20/filter.dict
> 

Extract pathes

> ./extract.sh ../linux-4.20

Concatinate all pathes into one (or two or more) file

> cat $(find ../linux-4.20 -name '*.path') > data/linux/raw.txt

Preprocess extracted pathes

> ./preprocess.sh linux

Show Help

> python cextractor.py --help

Display feature for inputting code2vec

> python cextractor.py aaa.c 

Display full path for debugging

> python cextractor.py aaa.c -p 

Display AST(Abstract syntax tree) for debugging

> python cextractor.py aaa.c -a
