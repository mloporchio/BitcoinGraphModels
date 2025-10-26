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
DEGREE_FILE = "pg/degree.tsv"
IN_DEGREE_FILENAME="pg_in_degree.tsv"
OUT_DEGREE_FILENAME="pg_out_degree.tsv"

df_tx_map = pl.read_csv(TRANSACTION_MAP_FILE, separator=",", has_header=False, new_columns=['tx_hash', 'tx_id'])
df_node_map = (
    pl.read_csv(NODE_MAP_FILE, separator="\t", has_header=False, new_columns=['tx_id:output_id', 'node_id']).with_columns(
        tx_id = pl.col('tx_id:output_id').str.split(":").list.first().cast(pl.Int64),
        output_id = pl.col('tx_id:output_id').str.split(":").list.last().cast(pl.Int64)
    )
).select("tx_id", "output_id", "node_id").join(df_tx_map, on="tx_id", how="left").drop("tx_id") # tx_hash, output_id, node_id

df_deg = pl.read_csv(DEGREE_FILE, separator="\t").join(df_node_map, on='node_id', how='left')

top_in = df_deg.sort("in_degree", descending=True).head(SIZE).select("node_id", "tx_hash", "output_id", "in_degree").with_row_index("rank")
top_out = df_deg.sort("out_degree", descending=True).head(SIZE).select("node_id", "tx_hash", "output_id", "out_degree").with_row_index("rank")

top_in.write_csv(OUTPUT_PATH + "/" + IN_DEGREE_FILENAME, null_value="null", separator="\t")
top_out.write_csv(OUTPUT_PATH + "/" + OUT_DEGREE_FILENAME, null_value="null", separator="\t")