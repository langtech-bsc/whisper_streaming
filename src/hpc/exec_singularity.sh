#!/bin/bash

CONTAINER=${1:-"/gpfs/projects/bsc88/singularity-images/s2st_dataset"}

# VERIFY CONTARINER EXISTS
[ ! -f $CONTAINER ] && echo -e "ERROR: Singularity container does not exist: [$CONTAINER]\nExiting..." && exit 

# LOAD SINGULARITY MODULE
cmd="module load singularity"
echo $cmd && eval $cmd

# ENTER CONTAINER
cmd="singularity exec --no-home --nv $CONTAINER bash"
echo $cmd && eval $cmd