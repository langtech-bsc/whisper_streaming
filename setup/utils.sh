#!/bin/bash


function log_msg(){

    local msg=$1
    echo -e "[$(date '+%Y-%m-%d %H:%M:%S')]\t$msg"

}

function load_config() {

    # LOAD CONFIG
    DELIM="##############################"
    local CONFIG=$1 # "$SCRIPT_DIR/project.config"
    [ ! -f $CONFIG ] && log_msg "ERROR: config files does not exist: $CONFIG" && log_msg "Exiting..." && exit
    . $CONFIG
    log_msg "$DELIM" && log_msg "Loading config in file $CONFIG" && cat $CONFIG && log_msg "$DELIM"

}

function allow_conda(){

    # TO BE ABLE CONDA INSIDE THE SCRIPT
    eval "$(conda shell.bash hook)"

}

function activate_env(){

    # ACTIVATE ENV
    cmd="conda activate $CONDA_ENV"
    log_msg "$cmd" && eval $cmd

}

function prepare_config_and_env(){

    local CONFIG=$1

    load_config $CONFIG
    allow_conda
    activate_env

}
