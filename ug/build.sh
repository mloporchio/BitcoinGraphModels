#!/bin/bash
#
#   This script builds the Bitcoin User Graph starting from the transaction list.
#   Author: Matteo Loporchio
#

INPUT_FILE="../data/tx_list.txt"
EL_FILE="el_orig.tsv"
EL_SORTED_FILE="el.tsv"
ADDRESS_GRAPH_EDGE_LIST="../ag/el.tsv"
AUX_GRAPH_BUILDER="./BitcoinAddressClustering/builder"
AUX_GRAPH_CLUSTER="./BitcoinAddressClustering/clustering"
AUX_GRAPH_FILE="./BitcoinAddressClustering/aux_graph"
CLUSTER_MAP_FILE="./BitcoinAddressClustering/comp.csv"
TRANSFORM_SCRIPT="transform.py"
TMP_DIR="tmp"

#eval "${AUX_GRAPH_BUILDER} ${INPUT_FILE} ${AUX_GRAPH_FILE}"

#eval "${AUX_GRAPH_CLUSTER} ${AUX_GRAPH_FILE} ${CLUSTER_MAP_FILE}"

python3 ${TRANSFORM_SCRIPT} ${ADDRESS_GRAPH_EDGE_LIST} ${CLUSTER_MAP_FILE} ${EL_FILE}

# Sort the edge list.
mkdir -p ${TMP_DIR}
((sort --temporary-directory=${TMP_DIR} -t$'\t' -k1,1n -k2,2n ${EL_FILE}) | uniq) > ${EL_SORTED_FILE}

# Remove the unsorted edge list and temporary directory.
rm -rf ${TMP_DIR} ${EL_FILE}