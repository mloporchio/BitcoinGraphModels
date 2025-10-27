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
NODE_MAP_FILE = "pg/nm.tsv"
HARMONIC_FILE = "download/harmonic/pg.txt"
OUTPUT_FILE = "pg_harmonic.tsv"

df_tx_map = pl.read_csv(TRANSACTION_MAP_FILE, separator=",", has_header=False, new_columns=['tx_hash', 'tx_id'])
df_node_map = (
    pl.read_csv(NODE_MAP_FILE, separator="\t", has_header=False, new_columns=['tx_id:output_id', 'node_id']).with_columns(
        tx_id = pl.col('tx_id:output_id').str.split(":").list.first().cast(pl.Int64),
        output_id = pl.col('tx_id:output_id').str.split(":").list.last().cast(pl.Int64)
    )
).select("tx_id", "output_id", "node_id").join(df_tx_map, on="tx_id", how="left").drop("tx_id") # tx_hash, output_id, node_id

df = (pl.read_csv(HARMONIC_FILE, separator="\t", has_header=False, new_columns=['node_id', 'harmonic'])
      .join(df_node_map, on='node_id', how='left'))

top = df.sort("harmonic", descending=True).head(SIZE).select("node_id", "tx_hash", "output_id", "harmonic").with_row_index("rank")
top.write_csv(OUTPUT_PATH + "/" + OUTPUT_FILE, null_value="null", separator="\t")