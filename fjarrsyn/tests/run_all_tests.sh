#!/bin/bash

export PYTHONPATH=${PWD/fjarrsyn\/tests/}:$PYTHONPATH
echo $PYTHONPATH

file_array=($(ls *.py))
for item in ${file_array[*]}
do
    python3 $item
done

