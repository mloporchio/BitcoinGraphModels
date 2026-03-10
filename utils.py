"""
Utility functions.
Authors: Matteo Loporchio
"""

import polars as pl

TXOUT_FILE = "data/tx_outputs.tsv"
TXIN_FILE = "data/tx_inputs.tsv"
COMP_FILE = "ug/comp.csv"
PAYMENT_MAP_FILE = "pg/nm.tsv"
MAP_ADDRESS_ID_FILE = "data/addr_id_map.csv"
MAP_TXHASH_ID_FILE = "data/txhash_id_map.csv"
MAP_ADDRESS_LABEL_FILE = "data/address_labels.tsv"
MAP_USER_LABEL_FILE = "data/comp_labels.json"
NUM_UNIQUE_ADDR = 293798168
MODELS = ["ag", "tg", "ug", "atg", "pg"]
METRICS = ["in_degree", "out_degree", "clustering", "pagerank", "harmonic"]

def get_node_type(model):
    if model == "ag":
        return "address"
    elif model == "tg":
        return "tx"
    elif model == "ug":
        return "comp"
    elif model == "atg":
        return "node"
    elif model == "pg":
        return "payment"
    else:
        raise ValueError(f"Unknown model: {model}")

def get_metric_filename(model, metric):
    """
    Returns the filename for the given model and metric.
    """
    assert (model in MODELS) and (metric in METRICS)
    if metric == "in_degree" or metric == "out_degree":
        return f"{model}/degree.tsv"
    if metric == "harmonic":
        return f"{model}/harmonic.parquet"
    return f"{model}/{metric}.tsv"

def load_metric_df(model, metric, columns=None):
    """
    Loads the dataframe for the given model and metric.
    """
    assert (model in MODELS) and (metric in METRICS)
    filename = get_metric_filename(model, metric)
    if metric == "harmonic":
        df = pl.read_parquet(filename)
        if not (columns is None):
            assert len(df.columns) == len(columns)
            df.columns = columns
        return df
    return pl.read_csv(filename, separator="\t", has_header=True, new_columns=columns)

def load_map_address_id(columns=None):
    """
    Loads the address -> address_id mapping file.
    """
    if columns is None:
        columns = ["address", "node_id"]
    return pl.read_csv(MAP_ADDRESS_ID_FILE, separator=",", has_header=False, new_columns=columns)

def load_map_txhash_id(columns=None):
    """
    Loads the tx_hash -> tx_id mapping file.
    """
    if columns is None:
        columns = ["tx_hash", "node_id"]
    return pl.read_csv(MAP_TXHASH_ID_FILE, separator=",", has_header=False, new_columns=columns)

def load_map_address_label(columns=None):
    """
    Loads the address -> label mapping file.
    """
    return pl.read_csv(MAP_ADDRESS_LABEL_FILE, separator="\t", has_header=True, new_columns=columns)

def load_map_user_label(columns=None):
    """
    Loads the user_id -> label mapping file.
    """
    return pl.read_ndjson(MAP_USER_LABEL_FILE).rename({'comp_id': 'node_id'})

def load_map_comp(columns=None):
    """
    Loads the address_id -> user_id mapping file
    """
    return pl.read_csv(COMP_FILE, separator=",", has_header=True, new_columns=columns)

def load_map_payments():
    """
    This function loads the node mapping file for the payment graph.
    The mapping associates each (tx_id, output_id) pair to a payment id (i.e., a node id in the graph).
    """
    return (
        pl.read_csv(PAYMENT_MAP_FILE, separator="\t", has_header=False, new_columns=['tx_id:output_id', 'payment_id']).with_columns(
            tx_id = pl.col('tx_id:output_id').str.split(":").list.first().cast(pl.Int64),
            output_id = pl.col('tx_id:output_id').str.split(":").list.last().cast(pl.Int64)
        )
    ).select("tx_id", "output_id", "payment_id")

def load_txout_df(columns=None):
    if columns is None:
        columns = ['tx_id', 'output_id', 'address_id']
    return pl.read_csv(TXOUT_FILE, separator="\t", has_header=False, new_columns=columns)