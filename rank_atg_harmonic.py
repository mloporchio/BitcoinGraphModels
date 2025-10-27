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
HARMONIC_FILE = "download/harmonic/atg.txt"
OUTPUT_FILE = "atg_harmonic.tsv"

df_lab = pl.read_csv(LABEL_MAP_FILE, separator="\t", has_header=True, new_columns=['entity', 'label'])
df_addr_map = (pl.read_csv(ADDRESS_MAP_FILE, separator=",", has_header=False, new_columns=['entity', 'node_id'])
               .with_columns(node_type = pl.lit("ADDRESS")))
df_tx_map = (pl.read_csv(TRANSACTION_MAP_FILE, separator=",", has_header=False, new_columns=['entity', 'node_id'])
             .with_columns(node_type = pl.lit("TX"), node_id = pl.col("node_id") + NUM_UNIQUE_ADDR))
df_map = pl.concat([df_addr_map, df_tx_map]).join(df_lab, on="entity", how="left") # entity, node_id, node_type, label
df = (pl.read_csv(HARMONIC_FILE, separator="\t", has_header=False, new_columns=['node_id', 'harmonic'])
      .join(df_map, on='node_id', how='left'))

top = (df.sort("harmonic", descending=True).head(SIZE)
       .select("node_id", "node_type", "entity", "label", "harmonic").with_row_index("rank"))
top.write_csv(OUTPUT_PATH + "/" + OUTPUT_FILE, null_value="null", separator="\t")