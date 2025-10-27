#
#
#
#   Author: Matteo Loporchio
#

import polars as pl
import sys

SIZE = int(sys.argv[1])
OUTPUT_PATH = sys.argv[2]
LABEL_MAP_FILE = "labels/comp_labels.json"
CLUSTERING_FILE = "ug/clustering.tsv"
OUTPUT_FILE = "ug_clustering.tsv"

df_lab = pl.read_ndjson(LABEL_MAP_FILE).rename({'comp_id':'node_id'}) # node_id -> label mapping
df_pr = pl.read_csv(CLUSTERING_FILE, separator="\t").join(df_lab, on='node_id', how='left') # node_id, pagerank

top = df_pr.sort("clustering", descending=True).head(SIZE).select("node_id", "label", "clustering").with_row_index("rank")
top.write_csv(OUTPUT_PATH + "/" + OUTPUT_FILE, null_value="null", separator="\t")
