#
#
#
#   Author: Matteo Loporchio
#

import polars as pl
import sys

SIZE = int(sys.argv[1])
OUTPUT_PATH = sys.argv[2]
LABEL_MAP_FILE = "labels/comp_labels.json"
HARMONIC_FILE = "download/harmonic/ug.txt"
OUTPUT_FILE = "ug_harmonic.tsv"

df_lab = pl.read_ndjson(LABEL_MAP_FILE).rename({'comp_id':'node_id'}) # node_id -> label mapping
df = (pl.read_csv(HARMONIC_FILE, separator="\t", has_header=False, new_columns=['node_id', 'harmonic'])
      .join(df_lab, on='node_id', how='left')) # node_id, pagerank

top = df.sort("harmonic", descending=True).head(SIZE).select("node_id", "label", "harmonic").with_row_index("rank")
top.write_csv(OUTPUT_PATH + "/" + OUTPUT_FILE, null_value="null", separator="\t")
