#!/bin/bash
#   Author: Matteo Loporchio
#   Date: 2025-05-27
#

EXPERIMENT_NAME="pagerank"
MODELS=("ag" "tg" "atg" "ug" "pg")
MODEL_NAMES=("Address Graph" "Transaction Graph" "Address-Transaction Graph" "User Graph" "Payment Graph")
FIGURES_DIR="figures"
TARBALL_FILE="${FIGURES_DIR}/${EXPERIMENT_NAME}.tar.gz"
SCRIPT_NAME="plot_${EXPERIMENT_NAME}.py"

mkdir -p ${FIGURES_DIR}

for i in "${!MODELS[@]}"; do
    MODEL=${MODELS[$i]}
    MODEL_NAME=${MODEL_NAMES[$i]}
    echo "Processing model: ${MODEL_NAME}..."
    INPUT_FILE="${MODEL}/${EXPERIMENT_NAME}.tsv"
    if [ ! -f "${INPUT_FILE}" ]; then
        echo "Error: input file ${INPUT_FILE} does not exist. Skipping ${MODEL_NAME}."
        continue
    fi
    OUTPUT_FILE="${FIGURES_DIR}/${MODEL}_${EXPERIMENT_NAME}.pdf"
    PLOT_TITLE="${MODEL_NAME} PageRank"
    python3 "${SCRIPT_NAME}" "${INPUT_FILE}" "${OUTPUT_FILE}" "${PLOT_TITLE}"
    echo "Done!"
done
echo "All models processed."

# Create a tarball of the figures
tar czf ${TARBALL_FILE} ${FIGURES_DIR}/*_${EXPERIMENT_NAME}.pdf
echo "Figures were archived in ${TARBALL_FILE}."