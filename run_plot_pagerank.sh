#!/bin/bash
#   Author: Matteo Loporchio
#   Date: 2025-05-27
#

MODELS=("ag" "tg" "atg" "ug" "pg")
FIGURES_DIR="figures"
TARBALL_FILE="${FIGURES_DIR}/pagerank.tar.gz"
SCRIPT_NAME="plot_pagerank.py"

mkdir -p ${FIGURES_DIR}

for MODEL in "${MODELS[@]}"; do
    echo "Processing model: ${MODEL}..."
    INPUT_FILE="${MODEL}/pagerank.tsv"
    OUTPUT_FILE="${FIGURES_DIR}/${MODEL}_pagerank.pdf"
    python3 "${SCRIPT_NAME}" "${INPUT_FILE}" "${OUTPUT_FILE}" "${MODEL}"
    echo "Done!"
done
echo "All models processed."

# Create a tarball of the figures
tar czf ${TARBALL_FILE} ${FIGURES_DIR}/*_pagerank.pdf
echo "Figures were archived in ${TARBALL_FILE}."