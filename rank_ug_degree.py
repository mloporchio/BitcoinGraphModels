import polars as pl
import sys

SIZE = int(sys.argv[1])
OUTPUT_PATH = sys.argv[2]
LABEL_MAP_FILE = "labels/comp_labels.json"
DEGREE_FILE = "ug/degree.tsv"
IN_DEGREE_FILENAME="ug_in_degree.tsv"
OUT_DEGREE_FILENAME="ug_out_degree.tsv"

df_lab = pl.read_ndjson(LABEL_MAP_FILE).rename({'comp_id':'node_id'}) # node_id -> label mapping
df_deg = pl.read_csv(DEGREE_FILE, separator="\t") # node_id, in_degree, out_degree
df_deg = df_deg.join(df_lab, on='node_id', how='left')

top_in = df_deg.sort("in_degree", descending=True).head(SIZE).select("node_id", "label", "in_degree").with_row_index("rank")
top_out = df_deg.sort("out_degree", descending=True).head(SIZE).select("node_id", "label", "out_degree").with_row_index("rank")

top_in.write_csv(OUTPUT_PATH + "/" + IN_DEGREE_FILENAME, null_value="null", separator="\t")
top_out.write_csv(OUTPUT_PATH + "/" + OUT_DEGREE_FILENAME, null_value="null", separator="\t")