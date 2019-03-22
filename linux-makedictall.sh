#!/bin/sh

python -W ignore totaldict.py $(find ../linux-4.20 -name '*.dict') > ../linux-4.20/index.dict
