#!/bin/bash

CONTAINER_DEFAULT="/gpfs/projects/bsc88/singularity-images/s2st_dataset_sandbox"
CONTAINER=${1:-$CONTAINER_DEFAULT}
ARGS=${2:-""} # --writable --bind /gpfs:/gpfs
COMMAND=${3:-"bash"}

if [[ "$CONTAINER" == "default" ]]; then
    CONTAINER=$CONTAINER_DEFAULT
fi

 
# VERIFY CONTAINER EXISTS
[ ! -d $CONTAINER ] && echo -e "ERROR: Singularity sandbox container does not exist: [$CONTAINER]\nExiting..." && exit 

# LOAD SINGULARITY MODULE
cmd="module load singularity"
echo $cmd && eval $cmd

# ENTER CONTAINER
cmd="singularity exec $ARGS --no-home --nv $CONTAINER \"$COMMAND\""
echo $cmd # && eval $cmd

###### TO WORK WITH IT, BUT CANNOT INSTALL (current command in the script)
# cmd="singularity exec --no-home --nv $CONTAINER bash"
###### TO INSTALL 
# cmd="singularity exec --writable --no-home --nv $CONTAINER bash"
###### TO INSTALL AND MOUNT VOLUMES
# cmd="singularity exec --writable --bind /gpfs:/gpfs --no-home --nv $CONTAINER bash"
###### 