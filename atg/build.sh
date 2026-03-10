#!/bin/bash
#
# This script builds the Bitcoin Address Transaction Graph from the original transaction list.
# Author: Matteo Loporchio
#

INPUT_FILE="../data/tx_list.txt"
NUM_UNIQUE_ADDR=293798168
EL_FILE="el_orig.tsv"
EL_SORTED_FILE="el.tsv"
TMP_DIR="tmp"
EDGE_LIST_BUILDER="AddressTxGraphEdgeListBuilder"
WEBGRAPH_BUILDER="../WebgraphBuilder.jar"
GRAPH_PATH="graph/atg"
BUILD_OUT="build_out.log"
BUILD_ERR="build_err.log"
GRAPH_OUT="graph_out.log"
GRAPH_ERR="graph_err.log"
CLASSPATH="../bin"

# Build the edge list.
java -cp "${CLASSPATH}" -Xmx200g ${EDGE_LIST_BUILDER} ${INPUT_FILE} ${EL_FILE} ${NUM_UNIQUE_ADDR} 1>${BUILD_OUT} 2>${BUILD_ERR}

# Sort the edge list.
mkdir -p ${TMP_DIR}
((sort --temporary-directory=${TMP_DIR} -t$'\t' -k1,1n -k2,2n ${EL_FILE}) | uniq) > ${EL_SORTED_FILE}

# Remove the unsorted edge list and temporary directory.
rm -rf ${TMP_DIR} ${EL_FILE}

# Build the graph in WebGraph format.
java -Xmx200g -jar ${WEBGRAPH_BUILDER} ${EL_SORTED_FILE} ${GRAPH_PATH} 1>${GRAPH_OUT} 2>${GRAPH_ERR}
