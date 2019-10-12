#!/bin/bash

export PYTHONPATH=${PWD/tests/}:$PYTHONPATH

file_array=($(ls *.py))
for item in ${file_array[*]}
do
    python3 $item
done

