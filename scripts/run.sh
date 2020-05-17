#!/bin/bash

# Run jython processing from unix cli
# Pietro Jomini

BASEDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )"/.. >/dev/null 2>&1 && pwd )"

# Check & create lib dir
LIB=$BASEDIR/lib/linux
if [[ ! -d $LIB ]]; then
    mkdir -p $LIB
fi

# Check if jar exists, if not install it
PROCESSING=$LIB/processing-py.jar
if [[ ! -f $PROCESSING ]]; then
    # Pre cleanup
    rm -rf $LIB/*
    
    # Get source from official source
    wget -O $LIB/processing.py-linux64.tgz http://py.processing.org/processing.py-linux64.tgz
    
    # Extract jar
    mkdir $LIB/processing.py-linux64
    tar -zxvf $LIB/processing.py-linux64.tgz -C $LIB/processing.py-linux64
    mv $LIB/processing.py-linux64/*/processing-py.jar $LIB

    # After cleanup
    rm $LIB/processing.py-linux64.tgz
    rm -rf $LIB/processing.py-linux64
fi

# Java jre
JAVA=`which java`
[[ -z "${JAVA// }" ]] &&  echo "NO JRE FOUND" && exit 1

# Target python
# Can by both .py and .pypd
TARGET=$1
[[ ! -f $TARGET ]] && echo "NO INPUT FILE" && exit 1

# Run the python target
echo "Running $TARGET"
$JAVA -Xms512m -Xmx1024m -jar $PROCESSING $TARGET