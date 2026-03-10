"""
Author: Matteo Loporchio
"""

import polars as pl
import sys

ADDRESS_GRAPH_EDGE_LIST = sys.argv[1] #'../ag/el.tsv'
CLUSTER_MAP_FILE = sys.argv[2] #'./comp.csv'
OUTPUT_FILE = sys.argv[3] #'./el.tsv'

el = pl.read_csv(ADDRESS_GRAPH_EDGE_LIST, separator='\t', has_header=False, new_columns=['src', 'dst'])
cluster_map = pl.read_csv(CLUSTER_MAP_FILE, separator=',', has_header=True)

result = el.join(cluster_map.rename({'node_id': 'src', 'comp_id': 'src_map'}), on='src', how='left')
result = result.join(cluster_map.rename({'node_id': 'dst', 'comp_id': 'dst_map'}), on='dst', how='left')
result = result.select(['src_map', 'dst_map']) # Keep only the mapped columns
result = result.filter(pl.col("src_map") != pl.col("dst_map")) # Remove self-loops
#result = result.sort(['src_map', 'dst_map']).unique(subset=['src_map', 'dst_map']) # Sort and remove duplicates
result.write_csv(OUTPUT_FILE, separator='\t', include_header=False)