#!/bin/bash
#
#   This script creates the list of transaction outputs starting from the Bitcoin
#   transaction list. The result is saved to a TSV file.
#
#   Author: Matteo Loporchio
#

SPLITTER="TxSplitter"
INPUT_FILE="data/tx_list.txt"
OUTPUT_FILE="data/tx_outputs.tsv"

java -cp "${CLASSPATH}" ${SPLITTER} "${INPUT_FILE}" "${OUTPUT_FILE}"
