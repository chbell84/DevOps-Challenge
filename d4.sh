#!/bin/bash
OLDIFS=$IFS
IFS=$'\n\r'
array=()
l=$( sed 's/\(.*,\)\("[^,]*\),\([^,]*"\)\(.*\)/\1\2|\3\4/' file )
for line in $l;
do
    IFS=$','
    outLine=$''
    for i in $line; do
#        tempIFS=$IFS
        IFS=$'\n'
#    read -ra i<<<"$i"
        i="${i/|/,}"
        if [[ -z "$outLine" ]]; then
            outLine=$i
#        echo $outLine
#        echo $i
        else
            outLine=$i','$outLine
#            echo $outLine
        fi
#    echo $i
#        IFS=$tempIFS
#        echo $outLine
    done
    echo $outLine
done>>outfile.csv
#done
IFS=$OLDIFS
