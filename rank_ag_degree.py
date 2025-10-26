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
DEGREE_FILE = "ag/degree.tsv"
IN_DEGREE_FILENAME="ag_in_degree.tsv"
OUT_DEGREE_FILENAME="ag_out_degree.tsv"

df_lab = pl.read_csv(LABEL_MAP_FILE, separator="\t")
df_map = pl.read_csv(ADDRESS_MAP_FILE, separator=",", has_header=False, new_columns=['address', 'node_id'])
df_deg = pl.read_csv(DEGREE_FILE, separator="\t").join(df_map, on='node_id', how='left').join(df_lab, on='address', how='left')

top_in = df_deg.sort("in_degree", descending=True).head(SIZE).select("node_id", "address", "label", "in_degree").with_row_index("rank")
top_out = df_deg.sort("out_degree", descending=True).head(SIZE).select("node_id", "address", "label", "out_degree").with_row_index("rank")

top_in.write_csv(OUTPUT_PATH + "/" + IN_DEGREE_FILENAME, null_value="null", separator="\t")
top_out.write_csv(OUTPUT_PATH + "/" + OUT_DEGREE_FILENAME, null_value="null", separator="\t")