#!/bin/bash

CONTAINER=${1:-"/gpfs/projects/bsc88/singularity-images/s2st_dataset"}

cmd="module load singularity"
echo $cmd && eval $cmd

cmd="singularity build --sandbox ${CONTAINER}_sandbox $CONTAINER"
echo $cmd && eval $cmd