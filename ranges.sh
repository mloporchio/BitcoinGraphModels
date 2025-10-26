#!/bin/bash

MODELS=("ag" "tg" "atg" "ug" "pg")
MEASURE="pagerank"
OUTPUT_FILE="${MEASURE}_ranges.tsv"
printf "model\tmin\tmax\n" > ${OUTPUT_FILE}
for MODEL in "${MODELS[@]}"; do
    INPUT_FILE="${MODEL}/${MEASURE}.tsv"
    if [ ! -f "${INPUT_FILE}" ]; then
        echo "Error: input file ${INPUT_FILE} does not exist. Skipping ${MODEL}."
        continue
    fi
    RESULT=$((datamash -H min 2 max 2 < "${INPUT_FILE}") | tail -n +2)
    MIN=$(echo $RESULT | cut -d' ' -f1)
    MAX=$(echo $RESULT | cut -d' ' -f2)
    printf "%s\t%s\t%s\n" "${MODEL}" "${MIN}" "${MAX}" >> ${OUTPUT_FILE}
done