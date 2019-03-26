#!/bin/sh 

DIRS='crypto include lib scripts usr arch drivers init mm security virt block firmware ipc net sound certs fs kernel samples tools'

mkdir -p data
mkdir -p data/linux
mkdir -p data/linux/raw

parallel --jobs 10 sh linux-gendir.sh ::: $DIRS
