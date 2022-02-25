#!/bin/sh
#
# Create zip installer for add-on
#

#
# Bump version number
#
MAJOR=`cat VERSION | sed 's/[0-9][0-9]*$//'`
NEWMINOR=`cat VERSION | sed 's/^.*\.\([0-9][0-9]*\)$/echo "$[ \1 + 1 ]"/'|/bin/sh`
echo ${MAJOR}${NEWMINOR} > VERSION
#
# Now package the whole thing
#
ADDON=`basename $(dirname $(readlink -f $0))`
VERSION=`cat VERSION`
OUTFILE=${ADDON}-${VERSION}.zip

sed -i "s/\(^<addon.*version=\"\)[^\"]*\(\".*\)/\1${VERSION}\2/" addon.xml

HERE=`pwd`
cd ..
zip -r ${OUTFILE} ${ADDON}/*
cd ${HERE}
