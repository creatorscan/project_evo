out=$1
if [ -n "$1" ]; then
	out_base=" is executed"
	echo $out$out_base | festival --tts
else
	echo "Please speak again, command not found" | festival --tts
fi	
