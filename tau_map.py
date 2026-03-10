"""
Author: Matteo Loporchio
"""

import rank_compare
import sys
import time

if __name__ == "__main__":
    model = sys.argv[1]
    metric = sys.argv[2]
    output_file = sys.argv[3]
    print(f'Computing mapping for model {model} and metric {metric}.')
    start_time = time.time()
    df_compare = rank_compare.rank_compare(model, "ag", metric)
    df_compare.write_parquet(output_file)
    elapsed = time.time() - start_time
    print(f'Mapping for model {model} and metric {metric} computed in {elapsed:.3f} seconds.')
    print(f'Mapping file written to: {output_file}.')