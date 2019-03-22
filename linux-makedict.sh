#!/bin/sh

DIRS=$(find ../linux-4.20 -type d)
parallel --jobs 10 sh linux-makedictdir.sh ::: $DIRS
