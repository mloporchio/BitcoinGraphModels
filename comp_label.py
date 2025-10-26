import polars as pl

ADDRESS_MAP_FILE = "/data/backup/safeBTC/mapAddr2Ids.csv"
USER_MAP_FILE = "ug/BitcoinAddressClustering/comp.csv"
LABEL_MAP_FILE = "labels/address_labels.tsv"
OUTPUT_FILE = "labels/comp_labels.json"

print("Reading data...", end=" ")
df_address_map = pl.read_csv(ADDRESS_MAP_FILE, separator=",", has_header=False, new_columns=['address', 'node_id']) # => address, node_id 
df_user_map = pl.read_csv(USER_MAP_FILE, has_header=True, separator=",") # => node_id, comp_id
df_label_map = pl.read_csv(LABEL_MAP_FILE, has_header=True, separator="\t") # => address, label
print("Done!")

print("Joining tables...", end=" ")
df1 = df_user_map.join(df_address_map, on="node_id", how="left") # => node_id, comp_id, address
df2 = df1.join(df_label_map, on="address", how="left") # => node_id, comp_id, address, label
print("Done!")

print("Computing result...", end=" ")
result = df2.group_by("comp_id").agg(pl.col("label").unique().alias("labels"))
result.write_ndjson(OUTPUT_FILE)
print("Done!")