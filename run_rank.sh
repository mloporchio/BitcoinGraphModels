#!/bin/bash
#
#   Script to run ranking computations for different graph models.
#   Usage: ./run_rank.sh <measure>
#   Author: Matteo Loporchio
#

MEASURE=$1
MEASURES=("degree" "pagerank" "clustering" "harmonic")
SIZE=10000 # Number of entries in the final ranking
MODELS=("ag" "tg" "ug" "atg" "pg") # List of model names
OUTPUT_DIR="rank" # Output directory where results will be saved

# Create output directory if it does not exist.
mkdir -p ${OUTPUT_DIR}

# Check if the provided measure is valid.
if [[ ! " ${MEASURES[@]} " =~ " ${MEASURE} " ]]; then
    echo "Error: Invalid measure '${MEASURE}'. Valid options are: ${MEASURES[*]}"
    exit 1
fi

for i in "${!MODELS[@]}"; do
    MODEL=${MODELS[$i]}
    echo "Processing ${MODEL}..."
    SCRIPT_NAME="rank_${MODEL}_${MEASURE}.py"
    python3 ${SCRIPT_NAME} ${SIZE} ${OUTPUT_DIR}
    echo "Done!"
done