#set +m

VAR=$1
expdir=~/Desktop/sree_proj/project/NLP/nnet3_libri_tcp
mdl=$expdir/exp/chain/tdnn_7b/final.mdl                                      
graph=$expdir/exp/chain/tdnn_7b/graph_demov2
online_dir=$expdir/exp/online
audio=$expdir/input.wav
                                                                                

# to decode the recording utterance                                             
(./../NLP/online2-tcp-nnet3-decode-faster --config=$online_dir/conf/online.conf \
	--print-args=false \
	--samp-freq=16000 --beam=15.0 --lattice-beam=6.0 --acoustic-scale=1.0 \
	--frames-per-chunk=20 \
	--extra-left-context-initial=0 \
	--frame-subsampling-factor=3 \
	--min-active=200 \
	--max-active=7000 \
	--port-num=5050 \
	$mdl $graph/HCLG.fst $graph/words.txt & ) &> /dev/null

#echo "Welcome to Virtual assistant demo. You can ask me to copy video, delete video, copy browsing, delete browsing and copy folder. Please SPEAK NOW within 5 seconds, I am Listening" | festival --tts
# to pass the recordings to TCP server                                          
if [[ $VAR == "1" ]]; then
	timeout 4s rec -r 16k -e signed-integer -c 1 -b 16 -t raw -q - | nc -N localhost 5050
	#exit 0
elif [[ $VAR == "2" ]]; then
	sox $audio -t raw -c 1 -b 16 -r 16k -e signed-integer - | nc -N localhost 5050
	exit 0
fi	

exit 0
