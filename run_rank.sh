#!/bin/bash
#
#   This script ranks the nodes of each graph model according to the specified metric.
#   
#   Usage: ./run_rank.sh <measure>
#   Author: Matteo Loporchio
#

METRIC=$1
METRICS=("degree" "pagerank" "clustering" "harmonic")
SIZE=10000 # Number of entries in the final ranking
MODELS=("ag" "tg" "ug" "atg" "pg") # List of model names
OUTPUT_DIR="results/rank" # Output directory where results will be saved
RANK_SCRIPT="rank.py" # Python script that performs the ranking for a given model and metric

# Create output directory if it does not exist.
mkdir -p ${OUTPUT_DIR}

# Check if the provided metric is valid.
if [[ ! " ${METRICS[@]} " =~ " ${METRIC} " ]]; then
    echo "Error: Invalid metric '${METRIC}'. Valid options are: ${METRICS[*]}"
    exit 1
fi

for i in "${!MODELS[@]}"; do
    MODEL=${MODELS[$i]}
    echo "Processing ${MODEL}..."
    python3 ${RANK_SCRIPT} ${MODEL} ${METRIC} ${SIZE} ${OUTPUT_DIR}
    echo "Done!"
done
