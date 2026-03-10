#!/bin/bash
#
#   This script builds the Bitcoin User Graph starting from the transaction list.
#   Author: Matteo Loporchio
#

INPUT_FILE="../data/tx_list.txt"
EL_FILE="el_orig.tsv"
EL_SORTED_FILE="el.tsv"
ADDRESS_GRAPH_EDGE_LIST="../ag/el.tsv"
AUX_GRAPH_BUILDER="../bin/BitcoinAddressClustering/builder"
AUX_GRAPH_CLUSTER="../bin/BitcoinAddressClustering/clustering"
AUX_GRAPH_FILE="./aux_graph"
CLUSTER_MAP_FILE="./comp.csv"
TRANSFORM_SCRIPT="transform.py"
TMP_DIR="tmp"
GRAPH_PATH="graph/ug"
GRAPH_OUT="graph_out.log"
GRAPH_ERR="graph_err.log"
WEBGRAPH_BUILDER="../jar/WebgraphBuilder.jar"

mkdir -p ${TMP_DIR}

# Build the auxiliary graph.
eval "${AUX_GRAPH_BUILDER} ${INPUT_FILE} ${AUX_GRAPH_FILE}"

# Run the clustering procedure on the auxiliary graph and produce the cluster map.
eval "${AUX_GRAPH_CLUSTER} ${AUX_GRAPH_FILE} ${CLUSTER_MAP_FILE}"

# 
python3 ${TRANSFORM_SCRIPT} ${ADDRESS_GRAPH_EDGE_LIST} ${CLUSTER_MAP_FILE} ${EL_FILE}

# Sort the edge list and remove duplicates.
((sort --temporary-directory=${TMP_DIR} -t$'\t' -k1,1n -k2,2n ${EL_FILE}) | uniq) > ${EL_SORTED_FILE}

# Remove the unsorted edge list and temporary directory.
rm -rf ${TMP_DIR} ${EL_FILE}

# Build the graph in WebGraph format.
java -Xmx200g -jar ${WEBGRAPH_BUILDER} ${EL_SORTED_FILE} ${GRAPH_PATH} 1>${GRAPH_OUT} 2>${GRAPH_ERR}
