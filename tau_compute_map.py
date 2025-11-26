import logging
import rank_compare
import sys
import time

model = sys.argv[1]
metric = sys.argv[2]
output_file = sys.argv[3]

logger = logging.getLogger(name="tau_compute_map")
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

logger.info('Computing mapping for model %s and metric %s.', model, metric)
start_time = time.time()
df_compare = rank_compare.rank_compare(model, "ag", metric)
df_compare.write_parquet(output_file)
elapsed = time.time() - start_time
logger.info('Mapping for model %s and metric %s computed in %.3f seconds.', model, metric, elapsed)
logger.info('Mapping file written to: %s.', output_file)