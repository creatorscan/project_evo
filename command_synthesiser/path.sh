# changing the project dir will reflect in all files
#export PROJECT_DIR="$HOME/Desktop/sree_proj/project"
export PROJECT_DIR=$(pwd)/../
#export OLD_PROJECT_DIR="$HOME/Desktop/sree_proj/project"
export OLD_PROJECT_DIR=$(pwd)/../
export MODEL_DIR="$PROJECT_DIR/NLP/nnet3_libri_tcp"
export ONLINE_DIR="$OLD_PROJECT_DIR/NLP/nnet3_libri_tcp"
export KALDI_DIR="$HOME/kaldi"

# defining all binaries and scripts in current environment
export PATH=$KALDI_DIR/src/online2bin:$PROJECT_DIR/NLP:$PROJECT_DIR/command_synthesiser:$PATH
