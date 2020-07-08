#!/bin/bash

# Loads jl file into a running elasticsearch instance on port localhost:9200
# Takes two arguemnts, the name of the index to be created and then the name of the input file.

if [ "$#" -ne 2 ]; then
    echo "Usage: takes two filename arguments"
exit 1
fi

curl -H "Content-Type: application/x-ndjson" -X POST http://localhost:9200/$1/_bulk --data-binary @$2
