#!/bin/sh

count=0
set epsname = ''
for aFile in `ls | grep gram |sed 's/\(.*\).gram/\1/'` 
do
  gramFile=`echo $aFile.gram`
  fsgFile=`echo $aFile.fsg`
  sam2p $pngFile EPS: $epsFile
  sphinx_jsgf2fsg -compile yes  -jsgf $gramFile > $fsgFile
  echo "$gramFile :fsg $fsgFile"
done
