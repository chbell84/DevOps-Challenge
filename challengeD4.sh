#!/bin/bash

##########################################################
#   DevOPs Challenge D4
#   Create a shell script that does the same steps as D1 Python script steps 1-3
#       and in addition create a file that reverses the text in every 3rd column.
#
#   This script accepts two parameters from the command line
#   1st a csv file
#   2nd a stock ticker (ex=AAPL)
#   The following 4 files are created in the local directory:
#       reverse_third_columns.csv
#       reversed_columns.csv
#       alternating_columns.csv
#       stock_data.csv
#  
##########################################################

# takes an array of data and prints out the columns in reverse order
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

# takes an array of data and prints out every other columns
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

# takes an array of data and prints out the columns in and reverses the order of
#   characters in every third column
reverse_third_columns() {
    IFS=$'\n\r'
    for line in $@;
    do
        IFS=$','
        outLine=$''
        i=1
        for column in $line; do
            IFS=$'\n'
            column="${column/|/,}"
            invert=$((i%3))
            i=$((i+1))
            if [[ $invert -eq 0 ]]; then
                tmp=""
                len=${#column}
                for ((j=0 ; j < $len ; j++)); do
                    tmp=${column:$j:1}$tmp
                done
                column=$tmp
#                echo $column
#                echo $tmp
            fi
            if [[ -z "$outLine" ]]; then
                outLine=$column
            else
                outLine=$outLine','$column
            fi
        done
        echo $outLine
    done
}

# takes an stock ticker and passes it to World Trading Data API
#   then saves a csv file of historical trading date for that stock
pull_stock_data(){
    url="https://api.worldtradingdata.com/api/v1/history?"
    symbol=$1
    api_token="pUZbiXpKgv1kqXkFMrWQdcqkAgzBpWAC2HAoHNW9EdAIHS7mEHOZixjFapME"
    url="${url}symbol=${symbol}&sort=newest&output=csv&api_token=${api_token}"
    echo $url
    echo "Pulling Historical Stock data for ${symbol}"
    curl ${url} > stock_data.csv
}


OLDIFS=$IFS
IFS=$'\n\r'
l=$( sed 's/\(.*,\)\("[^,]*\),\([^,]*"\)\(.*\)/\1\2|\3\4/' $1 )
reverse_third_columns $l > reverse_third_columns.csv
reverse_columns $l > reversed_columns.csv
alternate_columns $l > alternating_columns.csv
pull_stock_data $2
IFS=$OLDIFS
