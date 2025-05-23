#!/bin/bash

# PREPARE VARIABLES
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
PROJECT_DIR=$(realpath $SCRIPT_DIR/..)
CONFIG="$SCRIPT_DIR/project.config"
#WAV_FILE="../s2st_dataset/tests/data/wav/rXn1vkhUZZk_chunk.wav"
WAV_FILE="../s2st_dataset/tests/data/wav/rXn1vkhUZZk_chunk_300s.wav"
LEVEL="DEBUG"

# LOAD UTILS
. $SCRIPT_DIR/utils.sh

# RUN UTILS FUNCTIONS
prepare_config_and_env $CONFIG

# RUN TEST COMMAND
cd $PROJECT_DIR
PYTHON="whisper_online.py"
[ ! -f $PYTHON ] && log_msg "python script does not exist: $PYTHON" && log_msg "Exiting..." && exit
cmd="python3 $PYTHON $WAV_FILE --language en --min-chunk-size 1 -l $LEVEL | tee $PROJECT_DIR/output.log"
echo $cmd && eval $cmd


