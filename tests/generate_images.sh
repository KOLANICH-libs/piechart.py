#!/usr/bin/env sh
for i in `seq 1 9`; do python3 ./piechart.py 0.$i 0.1 > ./tests/images/0.$i.svg;done
