#!/bin/zsh

if [ -z "$1" ]; then
    echo "Error: select argument"
    exit 1
fi

run_number=$1

timestamp=$(date +"%Y%m%d_%H%M%S")

mkdir -p log/${run_number}

python3 src/prompt.py > log/${run_number}/${timestamp}.log 2>&1