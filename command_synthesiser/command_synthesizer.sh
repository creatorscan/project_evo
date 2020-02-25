#!/bin/bash

. ./path.sh || exit 1;

file=asr_out
VAR=$1

echo "Welcome to Virtual assistant demo. You can ask me to copy video, delete video, copy browsing, delete browsing and copy folder. Please SPEAK NOW within 5 seconds, I am Listening"
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



