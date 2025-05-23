#!/bin/bash

# PREPARE VARIABLES
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
CONFIG="$SCRIPT_DIR/project.config"

# LOAD UTILS
. $SCRIPT_DIR/utils.sh

# RUN UTILS FUNCTIONS
prepare_config_and_env $CONFIG

# INSTALL REQUIREMENTS
pip install librosa soundfile
pip install faster-whisper
pip install torch torchaudio

