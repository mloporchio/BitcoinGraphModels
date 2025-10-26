#!/bin/bash
#   This script processes degree data for various models and generates plots.
#   Author: Matteo Loporchio
#   Date: 2025-05-26
#


MODELS=("ag" "tg" "atg" "ug" "pg")
MODEL_NAMES=("Address Graph" "Transaction Graph" "Address-Transaction Graph" "User Graph" "Payment Graph")
FIGURES_DIR="figures"
TARBALL_FILE="${FIGURES_DIR}/degree.tar.gz"
SCRIPT_NAME="plot_degree.py"

mkdir -p ${FIGURES_DIR}

for i in "${!MODELS[@]}"; do
    MODEL=${MODELS[$i]}
    MODEL_NAME=${MODEL_NAMES[$i]}
    echo "Processing model: ${MODEL_NAME}..."
    INPUT_FILE="${MODEL}/degree.tsv"
    OUTPUT_FILE="${FIGURES_DIR}/${MODEL}_degree"
    python3 "${SCRIPT_NAME}" "${INPUT_FILE}" "${OUTPUT_FILE}" "${MODEL_NAME}"
    echo "Done!"
done
echo "All models processed."

# Create a tarball of the figures
tar czf ${TARBALL_FILE} ${FIGURES_DIR}/*_degree_*.pdf
echo "Figures were archived in ${TARBALL_FILE}."