#!/bin/bash
FILE_NAME=".tracker_md5sum"
TMP_NAME=".tracker_tmp"

if [[ $# < 1  ]]
then
    echo "Usage: $0 URL"
    echo "Return value: 1 when changed, 0 when the same."
    exit -1
fi

wget -q "$1" -O $TMP_NAME
result=`md5sum $TMP_NAME | awk '{ print $1 }'`
rm $TMP_NAME

if [ ! -f $FILE_NAME ]
then
    echo $result > $FILE_NAME
fi

previous=`cat $FILE_NAME`

if [ "$result" == "$previous" ]
then
    exit 1
else
    exit 0
fi
