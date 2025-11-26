#!/bin/bash

MODELS=("tg" "ug" "atg" "pg")
METRICS=("in_degree" "out_degree" "pagerank" "harmonic")
SCRIPT_MAP="tau_compute_map.py"
SCRIPT_SCORES="tau_compute_scores.py"
SCRIPT_METRIC="tau_compute_metric.py"
OUTPUT_DIR="test"

for MODEL in "${MODELS[@]}"; do
    for METRIC in "${METRICS[@]}"; do
        MAP_FILE="${OUTPUT_DIR}/map_${MODEL}_${METRIC}.parquet"
        SCORES_FILE="${OUTPUT_DIR}/scores_${MODEL}_${METRIC}.parquet"
        KT_FILE="${OUTPUT_DIR}/kt_${MODEL}_${METRIC}.tsv"
        echo "Processing metric ${METRIC} for model ${MODEL}..."
        # 
        python3 "${SCRIPT_MAP}" "${MODEL}" "${METRIC}" "${MAP_FILE}"
        #
        python3 "${SCRIPT_SCORES}" "${MODEL}" "${METRIC}" "${MAP_FILE}" "${SCORES_FILE}"
        #
        python3 "${SCRIPT_METRIC}" "${MODEL}" "${METRIC}" "${SCORES_FILE}" "${KT_FILE}"
        echo "Done!"
    done
    echo "All metrics processed for model ${MODEL}."
done