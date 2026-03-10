#!/bin/bash
# 
#   This script processes data for various models and generates plots.
#   The script accepts an experiment name as an argument 
#   (namely one of "connectivity", "degree", "pagerank", "harmonic") 
#   which determines the type of plot to generate.
#   
#   The generated plots are saved in the 'figures' directory and then archived into a tarball.
#   
#   Author: Matteo Loporchio
#

EXPERIMENT=$1
EXPERIMENTS=("connectivity" "degree" "pagerank" "harmonic")
MODELS=("ag" "tg" "atg" "ug" "pg")
FIGURES_DIR="figures"
TARBALL_FILE="${FIGURES_DIR}/${EXPERIMENT}.tar.gz"
SCRIPT_NAME="plot_${EXPERIMENT}.py"

# Check if the provided experiment name is valid.
if [[ ! " ${EXPERIMENTS[@]} " =~ " ${EXPERIMENT} " ]]; then
    echo "Error: Invalid experiment '${EXPERIMENT}'. Valid options are: ${EXPERIMENTS[*]}"
    exit 1
fi

mkdir -p ${FIGURES_DIR}

EXTENSION="tsv"
if [[ $EXPERIMENT == "harmonic" ]]; then
    EXTENSION="parquet"
fi

for MODEL in "${MODELS[@]}"; do
    echo "Processing model: ${MODEL}..."
    INPUT_FILE="${MODEL}/${EXPERIMENT}.${EXTENSION}"
    if [[ $EXPERIMENT == "degree" || $EXPERIMENT == "connectivity" ]]; then
        OUTPUT_FILE="${FIGURES_DIR}/${MODEL}_${EXPERIMENT}"
    else
        OUTPUT_FILE="${FIGURES_DIR}/${MODEL}_${EXPERIMENT}.pdf"
    fi
    python3 "${SCRIPT_NAME}" "${INPUT_FILE}" "${OUTPUT_FILE}" "${MODEL}"
    echo "Done!"
done
echo "All models processed."

# Create a tarball of the figures
if [[ $EXPERIMENT == "degree" || $EXPERIMENT == "connectivity" ]]; then
    tar czf ${TARBALL_FILE} ${FIGURES_DIR}/*_${EXPERIMENT}_*.pdf
else
    tar czf ${TARBALL_FILE} ${FIGURES_DIR}/*_${EXPERIMENT}.pdf
fi
#rm ${FIGURES_DIR}/*_${EXPERIMENT}*.pdf
echo "Figures were archived in ${TARBALL_FILE}."