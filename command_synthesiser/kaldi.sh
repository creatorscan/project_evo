#!/bin/bash

. ./path.sh || exit 1;

file=asr_out
VAR=$1

echo "Please SPEAK NOW, I am Listening" | festival --tts
bash nnet3_online.sh "$VAR" | grep "" &> $file

sed -e "s||\n|g" $file | sort -u > ${file}.toparse

# remove fillers
sed -i '/^$/d' ${file}.toparse
sed -i '/^ \+$/d' ${file}.toparse
sed -i "s|uh-huh||g;s|mhm||g" ${file}.toparse
sed -i "s@\[noise\]@@g" $file.toparse
sed -i "s@\[laughter\]@@g" $file.toparse
sed -i '/^$/d' ${file}.toparse
sed -i '/^ \+$/d' ${file}.toparse
sed -i ':a;N;$!ba;s/\n/ /g' ${file}.toparse
sed -i "s| \+| |g" ${file}.toparse
awk '{print tolower($0)}' ${file}.toparse > ${file}.parsed
