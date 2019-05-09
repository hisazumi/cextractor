 <!-- -*- coding: utf-8 -*- -->

# cextractor

## Setup
cextractor requires the clang python binding.

### for Mac

【install llvm】  
llvm(コンパイラのバックエンド)をインストール。

	brew install llvm
<br />
<br />

【install clang binding】  
clang(コンパイラのフロントエンド)をインストール。読み方はクラン。

	pip3 install clang  
<br />
<br />

【and set LD_LIBRARY_PATH】  
パスの設定。ライブラリの場所をlibに指定。

	export LD_LIBRARY_PATH=/usr/local/opt/llvm/lib
 
<br />
<br />

## How to Use

【Login】  
dl-box.localにssh接続。

	ssh dl-box.local  

<br />
<br />

【Directrory】
cextractorまで行く。

	/data2/c2v/cextractor


【Make dictionary】
一つ前に戻ってlinux-4.20に./dictmake.shの結果を出力 ここに辞書を作る。

	./dictmake.sh ../linux-4.20

<br />
<br />

【Filtering terms】  
linux-4.20の中のtotaldict(dictmakeで作ったやつ)を見て単語をフィルターにかけて結果をlinux-4.20のfilter.dictに出力する というのをdictfilter.pyで実行する。

	python dictfilter.py ../linux-4.20/total.dict > ../linux-4.20/filter.dict
> 

<br />
<br />

【Extract pathes】  
linux-4.20を読んでextract.shを実行しパスの抽出をする。

	./extract.sh ../linux-4.20

<br />
<br />

【Concatinate all pathes into one (or two or more) file】  
linux-4.20の中でpathという名前を見つけて結果をraw.txtに出力する。

	cat $(find ../linux-4.20 -name '*.path') > data/linux/raw.txt


<br />
<br />

【Preprocess extracted pathes】  
データ入力や整理といったプリプロセスを実行してlinuxというディレクトリに出力する。

	./preprocess.sh linux

<br />
<br />

【Show Help】  
ヘルプを表示する。

	python cextractor.py --help

<br />
<br />

【Display feature for inputting code2vec】  
code2vecへの入力の特徴を表示する。

	python cextractor.py aaa.c 

<br />
<br />

【Display full path for debugging】  
デバッグのためにフルパスを表示する。

	python cextractor.py aaa.c -p 

<br />
<br />

【Display AST(Abstract syntax tree) for debugging】  
デバッグのためにAST(抽象構文木)を表示する。

	python cextractor.py aaa.c -a
