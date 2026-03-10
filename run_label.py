"""
This script computes the mapping from a Bitcoin user to a list of labels,
based on the address labels and the mapping from addresses to users. 
The output is saved in a JSON file.

Author: Matteo Loporchio
"""

import polars as pl
import os

ADDRESS_MAP_FILE = "data/addr_id_map.csv"
USER_MAP_FILE = "ug/comp.csv"
LABEL_MAP_FILE = "data/address_labels.tsv"
OUTPUT_FILE = "data/comp_labels.json"

if __name__ == "__main__":
    # Check if the input files exist.
    for file in [ADDRESS_MAP_FILE, USER_MAP_FILE, LABEL_MAP_FILE]:
        if not os.path.exists(file):
            print(f"Error: File '{file}' not found.")
            exit(1)
    
    # Read the input files.
    print("Reading data...", end=" ")
    df_address_map = pl.read_csv(ADDRESS_MAP_FILE, separator=",", has_header=False, new_columns=['address', 'node_id']) # => address, node_id 
    df_user_map = pl.read_csv(USER_MAP_FILE, has_header=True, separator=",") # => node_id, comp_id
    df_label_map = pl.read_csv(LABEL_MAP_FILE, has_header=True, separator="\t") # => address, label
    print("Done!")

    # Join the tables to get the mapping from comp_id (i.e., user) to a list of labels.
    print("Computing result...", end=" ")
    df1 = df_user_map.join(df_address_map, on="node_id", how="left") # => node_id, comp_id, address
    df2 = df1.join(df_label_map, on="address", how="left") # => node_id, comp_id, address, label
    result = df2.group_by("comp_id").agg(pl.col("label").unique().alias("labels"))
    result.write_ndjson(OUTPUT_FILE)
    print("Done!")