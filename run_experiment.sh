#!/bin/bash
#
#   This script executes an experiment on a given graph model.
#   Possible experiments are: "degree", "connectivity", "pagerank".
#   Possible models are: "ag", "atg", "pg", "tg", "ug".
#
#   Usage: ./run_experiment.sh <experiment_name> <model_name>
#
#   Example: ./run_experiment.sh degree ag 
#   computes the in- and out-degree distributions of the Bitcoin Address Graph and 
#   saves the output in the `ag/degree.tsv` file. Logs are saved in the `log` folder.
#
#   Author: Matteo Loporchio
#

EXPERIMENT_NAME=$1
MODEL_NAME=$2

INPUT_FILE="${MODEL_NAME}/el.tsv"
OUTPUT_FILE="${MODEL_NAME}/${EXPERIMENT_NAME}.tsv"
LOG_DIR="./log"
LOG_OUTPUT="${LOG_DIR}/${EXPERIMENT_NAME}_output_${MODEL_NAME}.log"
LOG_ERROR="${LOG_DIR}/${EXPERIMENT_NAME}_error_${MODEL_NAME}.log"

mkdir -p ${LOG_DIR}

EXEC_NAME = "${EXPERIMENT_NAME}"
if [[ (${MODEL_NAME} == "tg" || ${MODEL_NAME} == "pg") && ${EXPERIMENT_NAME} == "pagerank" ]]; then
    EXEC_NAME="pagerank_dag"
fi

eval "./${EXEC_NAME} ${INPUT_FILE} ${OUTPUT_FILE} 1>${LOG_OUTPUT} 2>${LOG_ERROR}"



