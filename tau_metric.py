"""
This module computes the Weighted Kendall's Tau metric for a given model and metric, 
based on the scores computed by tau_scores.py.
Author: Matteo Loporchio
"""

import numpy as np
import polars as pl
import sys
import time
from scipy import stats

def kendall_tau(df_scores):
    x = df_scores['base'].to_numpy() # addr_id, base, target
    y = df_scores['target'].to_numpy()
    kt = stats.weightedtau(x, y, rank=None).statistic
    return kt
        
if __name__ == "__main__":
    model = sys.argv[1]
    metric = sys.argv[2]
    scores_file = sys.argv[3]
    kt_file = sys.argv[4]
    print(f'Computing KT for model {model} and metric {metric}.')
    start_time = time.time()
    df_scores = pl.read_parquet(scores_file)
    if metric == "harmonic":
        df_scores = df_scores.drop_nulls() # remove rows with null values for harmonic metric
    kt = kendall_tau(df_scores)
    elapsed = time.time() - start_time
    print(f'KT for model {model} and metric {metric} computed in {elapsed:.3f} seconds (result = {kt:.6f}).')
    with open(kt_file, 'w') as f:
        f.write(f"{kt:.6f}\t{elapsed:.3f}\n")
    print(f'KT result written to: {kt_file}.')
