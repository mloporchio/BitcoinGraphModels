#
#
#
#   Author: Matteo Loporchio
#

import polars as pl
import sys

SIZE = int(sys.argv[1])
OUTPUT_PATH = sys.argv[2]
NUM_UNIQUE_ADDR = 293798168 # This is also the first TX node identifier.
ADDRESS_MAP_FILE = "/data/backup/safeBTC/mapAddr2Ids.csv"
TRANSACTION_MAP_FILE = "/data/backup/safeBTC/mapTxHash2Ids.csv"
LABEL_MAP_FILE = "labels/address_labels.tsv"
DEGREE_FILE = "atg/degree.tsv"
IN_DEGREE_FILENAME="atg_in_degree.tsv"
OUT_DEGREE_FILENAME="atg_out_degree.tsv"

df_lab = pl.read_csv(LABEL_MAP_FILE, separator="\t", has_header=True, new_columns=['entity', 'label'])
df_addr_map = (pl.read_csv(ADDRESS_MAP_FILE, separator=",", has_header=False, new_columns=['entity', 'node_id'])
               .with_columns(node_type = pl.lit("ADDRESS")))
df_tx_map = (pl.read_csv(TRANSACTION_MAP_FILE, separator=",", has_header=False, new_columns=['entity', 'node_id'])
             .with_columns(node_type = pl.lit("TX"), node_id = pl.col("node_id") + NUM_UNIQUE_ADDR))
df_map = pl.concat([df_addr_map, df_tx_map]).join(df_lab, on="entity", how="left") # entity, node_id, node_type, label
df_deg = pl.read_csv(DEGREE_FILE, separator="\t").join(df_map, on='node_id', how='left')

top_in = df_deg.sort("in_degree", descending=True).head(SIZE).select("node_id", "node_type", "entity", "label", "in_degree").with_row_index("rank")
top_out = df_deg.sort("out_degree", descending=True).head(SIZE).select("node_id", "node_type", "entity", "label", "out_degree").with_row_index("rank")

top_in.write_csv(OUTPUT_PATH + "/" + IN_DEGREE_FILENAME, null_value="null", separator="\t")
top_out.write_csv(OUTPUT_PATH + "/" + OUT_DEGREE_FILENAME, null_value="null", separator="\t")