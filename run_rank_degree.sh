#!/bin/bash
#
#
#   Author: Matteo Loporchio
#

SIZE=10000 # Number of entries in the final ranking
MODELS=("ag" "tg" "ug" "atg" "pg") # List of model names
OUTPUT_DIR="rank" # Output directory where results will be saved

mkdir -p ${OUTPUT_DIR}

for i in "${!MODELS[@]}"; do
    MODEL=${MODELS[$i]}
    echo "Processing $MODEL..."
    SCRIPT_NAME="rank_${MODEL}_degree.py"
    python3 ${SCRIPT_NAME} ${SIZE} ${OUTPUT_DIR}
    echo "Done!"
done