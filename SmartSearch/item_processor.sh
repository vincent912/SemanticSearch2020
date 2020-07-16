#!/bin/bash

# Processes a file of scraped entries taken from mist.com and filters out all non
# documentation pages and special characters and entries with empty snippets.
# Takes two arguemnts, the name of the input file and then the name of the output file.

if [ "$#" -ne 2 ]; then
    echo "Usage: takes two filename arguments"
exit 1
fi

sed '/.*www.mist.com\/documentation.*/!d' $1 | sed 's/\\u....//g' | sed 's/\\n//g' | sed '/.*"snippet": "".*/d' > $2


