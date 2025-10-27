#
#
#
#   Author: Matteo Loporchio
#

import polars as pl
import sys

SIZE = int(sys.argv[1])
OUTPUT_PATH = sys.argv[2]
TRANSACTION_MAP_FILE = "/data/backup/safeBTC/mapTxHash2Ids.csv"
CLUSTERING_FILE = "tg/clustering.tsv"
OUTPUT_FILE = "tg_clustering.tsv"

df_map = pl.read_csv(TRANSACTION_MAP_FILE, separator=",", has_header=False, new_columns=['tx_hash', 'node_id'])
df_pr = pl.read_csv(CLUSTERING_FILE, separator="\t").join(df_map, on='node_id', how='left')

top = df_pr.sort("clustering", descending=True).head(SIZE).select("node_id", "tx_hash", "clustering").with_row_index("rank")
top.write_csv(OUTPUT_PATH + "/" + OUTPUT_FILE, separator="\t")