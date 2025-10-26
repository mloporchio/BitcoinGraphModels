#!/bin/bash

MODELS=("ag" "tg" "atg" "ug" "pg")
MEASURES=("degree" "connectivity" "pagerank")
STATS_DIR="stats"
STATS_SCRIPT="stats.py"
OUTPUT_FORMAT="xlsx"

mkdir -p ${STATS_DIR}

for MODEL in "${MODELS[@]}"; do
    echo "Processing model: ${MODEL}..."
    for MEASURE in "${MEASURES[@]}"; do
        INPUT_FILE="${MODEL}/${MEASURE}.tsv"
        OUTPUT_FILE="${STATS_DIR}/${MODEL}_${MEASURE}_stats.${OUTPUT_FORMAT}"
        if [[ ! -f "${INPUT_FILE}" ]]; then
            echo "Input file ${INPUT_FILE} does not exist. Skipping..."
            continue
        fi
        python3 ${STATS_SCRIPT} "${INPUT_FILE}" "${OUTPUT_FILE}"
    done
done