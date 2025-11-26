#!/bin/bash
#   This script processes degree data for various models and generates plots.
#   Author: Matteo Loporchio
#   Date: 2025-05-26
#


MODELS=("ag" "tg" "atg" "ug" "pg")
FIGURES_DIR="figures"
TARBALL_FILE="${FIGURES_DIR}/connectivity.tar.gz"
SCRIPT_NAME="plot_connectivity.py"

mkdir -p ${FIGURES_DIR}

for MODEL in "${MODELS[@]}"; do
    echo "Processing model: ${MODEL}..."
    INPUT_FILE="${MODEL}/connectivity.tsv"
    OUTPUT_FILE="${FIGURES_DIR}/${MODEL}_connectivity"
    python3 "${SCRIPT_NAME}" "${INPUT_FILE}" "${OUTPUT_FILE}" "${MODEL}"
    echo "Done!"
done
echo "All models processed."

# Create a tarball of the figures
tar czf ${TARBALL_FILE} ${FIGURES_DIR}/*_connectivity_*.pdf
echo "Figures were archived in ${TARBALL_FILE}."