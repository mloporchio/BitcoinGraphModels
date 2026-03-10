#!/bin/bash
#
#   This script builds the Bitcoin Transaction Graph starting from the transaction list.
#   Author: Matteo Loporchio
#


INPUT_FILE="../data/tx_list.txt"
EL_FILE="el_orig.tsv"
EL_SORTED_FILE="el.tsv"
TMP_DIR="tmp"
EDGE_LIST_BUILDER="TxGraphEdgeListBuilder"
WEBGRAPH_BUILDER="../jar/WebgraphBuilder.jar"
GRAPH_PATH="graph/tg"
BUILD_OUT="build_out.log"
BUILD_ERR="build_err.log"
GRAPH_OUT="graph_out.log"
GRAPH_ERR="graph_err.log"
CLASSPATH="../bin"

# Build the edge list.
java -cp "${CLASSPATH}" -Xmx200g ${EDGE_LIST_BUILDER} ${INPUT_FILE} ${EL_FILE} 1>${BUILD_OUT} 2>${BUILD_ERR}

# Sort the edge list.
mkdir -p ${TMP_DIR}
((sort --temporary-directory=${TMP_DIR} -t$'\t' -k1,1n -k2,2n ${EL_FILE}) | uniq) > ${EL_SORTED_FILE}

# Remove the unsorted edge list and temporary directory.
rm -rf ${TMP_DIR} ${EL_FILE}

# Build the graph in WebGraph format.
java -Xmx200g -jar ${WEBGRAPH_BUILDER} ${EL_SORTED_FILE} ${GRAPH_PATH} 1>${GRAPH_OUT} 2>${GRAPH_ERR}
