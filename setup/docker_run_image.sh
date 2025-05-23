#!/bin/bash


SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
PROJECT_DIR=$(realpath $SCRIPT_DIR/../../)

cd $PROJECT_DIR/whisper_ctranslate2
mkdir -p docker_output
# --gpus "device=0" \
cmd="docker run \
    -v "$(pwd)":/srv/files/ \
    -it ghcr.io/softcatala/whisper-ctranslate2:latest \
    /srv/files/e2e-tests/gossos.mp3 \
    --output_dir /srv/files/docker_output"
echo $cmd && eval $cmd