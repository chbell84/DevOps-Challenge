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
        for i in $line; do
            IFS=$'\n'
            i="${i/|/,}"
            if [[ -z "$outLine" ]]; then
                outLine=$i
            else
                outLine=$i','$outLine
            fi
        done
        echo $outLine
    done
}

#echo $l
reverse_columns $l > reversed_columns.csv
#for line in $l;
#do
#    IFS=$','
#    outLine=$''
#    for i in $line; do
#        IFS=$'\n'
#        i="${i/|/,}"
#        if [[ -z "$outLine" ]]; then
#            outLine=$i
#        else
#            outLine=$i','$outLine
#        fi
#    done
#    echo $outLine
#done>reversed_columns.csv

#done
IFS=$OLDIFS
