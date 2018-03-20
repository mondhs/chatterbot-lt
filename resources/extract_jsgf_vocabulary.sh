#!/bin/sh

if [ $# -ne 1 ]
then
  echo "Usage: `basename $0` jsgf"
  exit 65
fi

sphinx_jsgf2fsg -jsgf $1 2>/dev/null | egrep "^TRANSITION( +\S+){4}$" | awk '{print($5)}' | sort | uniq | tee /tmp/words.txt

/home/mondhs/src/speech/sphinx/sphinx_liepa_train_docker/opt/sphinx_liepa_train/tool_data_prep/transcriber_re.py -i /tmp/words.txt -o /tmp/liepa-lt-lt.dict
