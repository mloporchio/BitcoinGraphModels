import utils
import rank_compare
import numpy as np
import polars as pl
import sys
import time
import logging
from scipy import stats

SIZES = [1e1, 1e2, 1e3, 1e4, 1e5, 1e6, 1e7]

logger = logging.getLogger(name="tau_compute_metric")

def compute_kt(scores_file, kt_file):
    df_scores = pl.read_parquet(scores_file)
    x = df_scores['base'].to_numpy() # addr_id, base, target
    y = df_scores['target'].to_numpy()
    with open(kt_file, "w") as f:
        for s in SIZES:
            x_r = x[:int(s)]
            y_r = y[:int(s)]
            kt = stats.weightedtau(x_r, y_r, rank=None).statistic
            f.write(f"{s}\t{kt}\n")
        kt = stats.weightedtau(x, y, rank=None).statistic
        f.write(f"{len(x)}\t{kt}")
        
if __name__ == "__main__":
    model = sys.argv[1]
    metric = sys.argv[2]
    scores_file = sys.argv[3]
    kt_file = sys.argv[4]
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    logger.info('Computing KT for model %s and metric %s.', model, metric)
    start_time = time.time()
    compute_kt(scores_file, kt_file)
    elapsed = time.time() - start_time
    logger.info('KT for model %s and metric %s computed in %.3f seconds.', model, metric, elapsed)
    logger.info('Output file written to: %s.', kt_file)