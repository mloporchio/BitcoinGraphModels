"""
This script ranks the nodes in the given model based on the given metric and saves the result as a TSV file.
Usage:
python rank.py <model> <metric> <size> <output_path>
- model: the graph model to rank (ag, tg, ug, atg, pg)
- metric: the metric to rank by (degree, pagerank, harmonic)
- size: the number of top nodes to save (-1 for all)
- output_path: the directory to save the output TSV file

Author: Matteo Loporchio
"""

import polars as pl
import utils
import sys

def rank(model, metric):
    """
    Ranks the nodes in the given model based on the given metric.
    Returns a dataframe with the following columns:
    - rank: the rank of the node (starting from 0)
    - node_id: the id of the node
    - additional columns depending on the model:
        - ag: address, label
        - tg: tx_hash
        - ug: label
        - atg: node_type, entity, label
        - pg: tx_hash, output_id
    - metric: the value of the metric
    """
    assert (model in utils.MODELS) and (metric in utils.METRICS)
    result = None
    metric_df = utils.load_metric_df(model, metric).select(["node_id", metric]) # node_id, metric
    if model == "ag":
        address_id_df = utils.load_map_address_id() # address, node_id
        address_label_df = utils.load_map_address_label() # address, label
        result = (metric_df.sort(metric, descending=True)
                  .join(address_id_df, on='node_id', how='left')
                  .join(address_label_df, on='address', how='left')
                  .select("node_id", "address", "label", metric).with_row_index("rank"))
    elif model == "tg":
        txhash_id_df = utils.load_map_txhash_id() # tx_hash, node_id
        result = (metric_df.sort(metric, descending=True)
                  .join(txhash_id_df, on='node_id', how='left')
                  .select("node_id", "tx_hash", metric).with_row_index("rank"))
    elif model == "ug":
        user_label_df = utils.load_map_user_label() # node_id, label    
        result = (metric_df.sort(metric, descending=True)
                  .join(user_label_df, on='node_id', how='left')
                  .select("node_id", "label", metric).with_row_index("rank"))
    elif model == "atg":
        address_label_df = utils.load_map_address_label(columns=["entity", "label"]) # address, label
        address_id_df = (utils.load_map_address_id(columns=["entity", "node_id"])
                         .with_columns(node_type = pl.lit("ADDRESS"))) # address, node_id
        txhash_id_df = (utils.load_map_txhash_id(columns=["entity", "node_id"])
                        .with_columns(node_type = pl.lit("TX"), 
                                      node_id = pl.col("node_id") + utils.NUM_UNIQUE_ADDR)) # tx_hash, node_id
        df_map = pl.concat([address_id_df, txhash_id_df]).join(address_label_df, on="entity", how="left") # entity, node_id, node_type, label
        result = (metric_df.sort(metric, descending=True)
                  .join(df_map, on='node_id', how='left')
                  .select("node_id", "node_type", "entity", "label", metric).with_row_index("rank"))
    elif model == "pg":
        paymap_df = utils.load_map_payments().rename({'payment_id' : 'node_id'}) # tx_id, output_id, node_id
        txhash_id_df = utils.load_map_txhash_id(columns=['tx_hash', 'tx_id']) # tx_hash, tx_id
        result = (metric_df.sort(metric, descending=True) # node_id, metric
                  .join(paymap_df, on='node_id', how='left') # node_id, metric, tx_id, output_id
                  .join(txhash_id_df, on='tx_id', how='left') # node_id, metric, tx_id, output_id, tx_hash
                  .select("node_id", "tx_hash", "output_id", metric).with_row_index("rank"))
    else:
        raise ValueError(f"Unknown model: {model}")
    return result

if __name__ == "__main__":
    model = sys.argv[1]
    metric = sys.argv[2]
    size = int(sys.argv[3])
    output_path = sys.argv[4]
    ranked_df = rank(model, metric)
    if size != -1:
        ranked_df = ranked_df.head(size)
    ranked_df.write_csv(f"{output_path}/{model}_{metric}.tsv", null_value="null", separator="\t")