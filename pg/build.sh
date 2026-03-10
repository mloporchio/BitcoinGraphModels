#!/bin/bash
#
#   This script builds the Bitcoin Payment Graph starting from the transaction list.
#   Author: Matteo Loporchio
#

INPUT_FILE="../data/tx_list.txt"
NM_FILE="nm.tsv"
EL_FILE="el_orig.tsv"
EL_SORTED_FILE="el.tsv"
TMP_DIR="tmp"
EDGE_LIST_BUILDER="PaymentGraphEdgeListBuilder"
WEBGRAPH_BUILDER="../jar/WebgraphBuilder.jar"
OUTPUT_PREFIX="graph/pg"
CLASSPATH="../bin"

# Parse the input file and create the edge list.
java -cp "${CLASSPATH}" -Xmx200g ${EDGE_LIST_BUILDER} ${INPUT_FILE} ${NM_FILE} ${EL_FILE} 1>elb_output.log 2>elb_errors.log

# Sort the TSV edge list.
mkdir -p ${TMP_DIR}
(sort --temporary-directory=tmp -t$'\t' -k1,1n -k2,2n ${EL_FILE} | uniq) > ${EL_SORTED_FILE}

# Remove the unsorted edge list and temporary directory.
rm -rf ${TMP_DIR} ${EL_FILE}

# Transform the TSV edge list into the WebGraph representation.
java -Xmx200g -jar ${WEBGRAPH_BUILDER} ${INPUT_FILE} ${OUTPUT_PREFIX} 1>wgb_output.log 2>wgb_errors.log