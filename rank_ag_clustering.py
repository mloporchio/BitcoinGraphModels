#
#
#
#   Author: Matteo Loporchio
#

import polars as pl
import sys

SIZE = int(sys.argv[1])
OUTPUT_PATH = sys.argv[2]
ADDRESS_MAP_FILE = "/data/backup/safeBTC/mapAddr2Ids.csv"
LABEL_MAP_FILE = "labels/address_labels.tsv"
CLUSTERING_FILE = "ag/clustering.tsv"
OUTPUT_FILE = "ag_clustering.tsv"

df_lab = pl.read_csv(LABEL_MAP_FILE, separator="\t")
df_map = pl.read_csv(ADDRESS_MAP_FILE, separator=",", has_header=False, new_columns=['address', 'node_id'])
df_pr = pl.read_csv(CLUSTERING_FILE, separator="\t").join(df_map, on='node_id', how='left').join(df_lab, on='address', how='left')

top = df_pr.sort("clustering", descending=True).head(SIZE).select("node_id", "address", "label", "clustering").with_row_index("rank")
top.write_csv(OUTPUT_PATH + "/" + OUTPUT_FILE, null_value="null", separator="\t")