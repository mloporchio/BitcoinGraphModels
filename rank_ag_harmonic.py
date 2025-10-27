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
HARMONIC_FILE = "download/harmonic/ag.txt"
OUTPUT_FILE = "ag_harmonic.tsv"

df_lab = pl.read_csv(LABEL_MAP_FILE, separator="\t")
df_map = pl.read_csv(ADDRESS_MAP_FILE, separator=",", has_header=False, new_columns=['address', 'node_id'])
df = (pl.read_csv(HARMONIC_FILE, separator="\t", has_header=False, new_columns=['node_id', 'harmonic'])
      .join(df_map, on='node_id', how='left').join(df_lab, on='address', how='left'))

top = df.sort("harmonic", descending=True).head(SIZE).select("node_id", "address", "label", "harmonic").with_row_index("rank")
top.write_csv(OUTPUT_PATH + "/" + OUTPUT_FILE, null_value="null", separator="\t")