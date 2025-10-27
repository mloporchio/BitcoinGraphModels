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
HARMONIC_FILE = "download/harmonic/tg.txt"
OUTPUT_FILE = "tg_harmonic.tsv"

df_map = pl.read_csv(TRANSACTION_MAP_FILE, separator=",", has_header=False, new_columns=['tx_hash', 'node_id'])
df = (pl.read_csv(HARMONIC_FILE, separator="\t", has_header=False, new_columns=['node_id', 'harmonic'])
      .join(df_map, on='node_id', how='left'))

top = df.sort("harmonic", descending=True).head(SIZE).select("node_id", "tx_hash", "harmonic").with_row_index("rank")
top.write_csv(OUTPUT_PATH + "/" + OUTPUT_FILE, separator="\t")