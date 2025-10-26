import polars as pl
import sys
import rank_utils

SIZE = int(sys.argv[1])
OUTPUT_PATH = sys.argv[2]
TRANSACTION_MAP_FILE = "/data/backup/safeBTC/mapTxHash2Ids.csv"
DEGREE_FILE = "tg/degree.tsv"
IN_DEGREE_FILENAME="tg_in_degree.tsv"
OUT_DEGREE_FILENAME="tg_out_degree.tsv"

df_map = pl.read_csv(TRANSACTION_MAP_FILE, separator=",", has_header=False, new_columns=['tx_hash', 'node_id'])
df_deg = pl.read_csv(DEGREE_FILE, separator="\t").join(df_map, on='node_id', how='left')

top_in = df_deg.sort("in_degree", descending=True).head(SIZE).select("node_id", "tx_hash", "in_degree").with_row_index("rank")
top_out = df_deg.sort("out_degree", descending=True).head(SIZE).select("node_id", "tx_hash", "out_degree").with_row_index("rank")

top_in.write_csv(OUTPUT_PATH + "/" + IN_DEGREE_FILENAME, separator="\t")
top_out.write_csv(OUTPUT_PATH + "/" + OUT_DEGREE_FILENAME, separator="\t")