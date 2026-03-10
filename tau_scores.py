"""
Author: Matteo Loporchio
"""

import utils
import rank_compare
import polars as pl
import sys
import time

def compute_scores(model, metric, map_file):
    node_type = rank_compare.get_node_type(model)
    df_compare = pl.read_parquet(map_file)
    # Load the address graph metric dataframe.
    base_metric_df = (utils.load_metric_df("ag", metric).select("node_id", metric).rename({"node_id" : "address_id", metric : f"{metric}_ag"})) # address_id, metric_ag
    # Load the target model metric dataframe.
    target_metric_df = (utils.load_metric_df(model, metric)
                        .select("node_id", metric)
                        .rename({"node_id" : f"{node_type}_id", metric : f"{metric}_{model}"}))
    #
    res = (df_compare.join(base_metric_df, on="address_id", how="left")
           .join(target_metric_df, on=f"{node_type}_id", how="left")
           .select(f"{node_type}_id", f"{metric}_{model}", "address_id", f"{metric}_ag")
           .group_by("address_id")
           .agg(pl.col(f"{metric}_ag").first().alias("base"), pl.col(f"{metric}_{model}").max().alias("target"))
           .sort("base", descending=True))
    return res

if __name__ == "__main__":
    model = sys.argv[1]
    metric = sys.argv[2]
    map_file = sys.argv[3]
    scores_file = sys.argv[4]
    print(f'Computing scores for model {model} and metric {metric}.')
    start_time = time.time()
    scores = compute_scores(model, metric, map_file)
    scores.write_parquet(scores_file)
    elapsed = time.time() - start_time
    print(f'Scores for model {model} and metric {metric} computed in {elapsed:.3f} seconds.')
    print(f'Output file written to: {scores_file}.')