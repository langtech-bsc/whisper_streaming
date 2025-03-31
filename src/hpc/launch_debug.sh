#!/bin/sh
#SBATCH --job-name="sandbox_s2st_demo"
#SBATCH -D .
#SBATCH --output=/gpfs/projects/bsc88/apps/marti/projects/whisper_streaming/logs/%x_%j.out  
#SBATCH --error=/gpfs/projects/bsc88/apps/marti/projects/whisper_streaming/logs/%x_%j.err  
#SBATCH --gres=gpu:4
#SBATCH --cpus-per-task=20
#SBATCH --nodes=1
#SBATCH -t 02:00:00
#SBATCH --qos acc_debug
#SBATCH --account bsc88
#SBATCH --exclusive

#####################
# PREPARE VARIABLES #
#####################
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
PROJECT_DIR=$(realpath $SCRIPT_DIR/../../)
WAV_FILE="/gpfs/projects/bsc88/apps/marti/projects/s2st_dataset/tests/data/wav/rXn1vkhUZZk_chunk.wav"
PYTHON="whisper_online.py"
LEVEL="DEBUG"
MODEL="projecte-aina/faster-whisper-large-v3-ca-3catparla" # "large-v2" # "projecte-aina/faster-whisper-large-v3-ca-3catparla"
TARGET_LANGUAGE="ca"
cmd="source export_env_variables_mn.sh && \
    python3 $PYTHON $WAV_FILE --language $TARGET_LANGUAGE --min-chunk-size 1 -l $LEVEL --model $MODEL 2>&1 > output.log"
##############################
# LAUNCH SINGULARITY SANDBOX #
##############################
module load singularity
singularity exec --no-home \
                 --nv /gpfs/projects/bsc88/singularity-images/s2st_dataset_sandbox \
                 bash -c "$cmd"

