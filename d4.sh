#!/bin/bash
OLDIFS=$IFS
IFS=$'\n\r'
array=()
l=$( sed 's/\(.*,\)\("[^,]*\),\([^,]*"\)\(.*\)/\1\2|\3\4/' file )

reverse_columns() {
    IFS=$'\n\r'
    for line in $@;
    do
        IFS=$','
        outLine=$''
        for column in $line; do
            IFS=$'\n'
            column="${column/|/,}"
            if [[ -z "$outLine" ]]; then
                outLine=$column
            else
                outLine=$column','$outLine
            fi
        done
        echo $outLine
    done
}

alternate_columns() {
    IFS=$'\n\r'
    for line in $@;
    do
        IFS=$','
        outLine=$''
        i=0
        for column in $line; do
            IFS=$'\n'
            column="${column/|/,}"
            no_skip=$((i%2))
            i=$((i+1))
            if [[ $no_skip -eq 0 ]]; then
                if [[ -z "$outLine" ]]; then
                    outLine=$column
                else
                    outLine=$outLine','$column
                fi
            fi
        done
        echo $outLine
    done
}

reverse_columns $l > reversed_columns.csv
alternate_columns $l > alternating_columns.csv
IFS=$OLDIFS
