import polars as pl

TXOUT_FILE = "data/tx_outputs.tsv"
TXIN_FILE = "data/tx_inputs.tsv"
COMP_FILE = "ug/BitcoinAddressClustering/comp.csv"
PAYMENT_MAP_FILE = "pg/nm.tsv"
NUM_UNIQUE_ADDR = 293798168

MODELS = ["ag", "tg", "ug", "atg", "pg"]
METRICS = ["in_degree", "out_degree", "pagerank", "harmonic"]

def get_metric_filename(model, metric):
    assert (model in MODELS) and (metric in METRICS)
    if metric == "in_degree" or metric == "out_degree":
        return f"{model}/degree.tsv"
    return f"{model}/{metric}.tsv"

def load_metric_df(model, metric, columns = None):
    assert (model in MODELS) and (metric in METRICS)
    if columns is None:
        return pl.read_csv(get_metric_filename(model, metric), separator="\t", has_header=True)
    return pl.read_csv(get_metric_filename(model, metric), separator="\t", has_header=True, new_columns=columns)

def load_txout_df():
    return pl.read_csv(TXOUT_FILE, separator="\t", has_header=False, new_columns=['tx_id', 'output_id', 'address_id'])

def load_comp_df():
    return pl.read_csv(COMP_FILE, separator=",", has_header=True)

def load_paymap_df():
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

def compute_rank(model, metric):
    assert (model in MODELS) and (metric in METRICS)
    metric_df = load_metric_df(model, metric)
    ranked_df = metric_df.select("node_id", metric).sort(metric, descending=True).with_row_index("rank")
    return ranked_df

def tg_to_ag(metric):
    assert metric in METRICS
    tx_outputs = load_txout_df() # Read the transaction output list.
    columns = None
    if metric == "in_degree":
        columns = ["tx_id", "in_degree_tg", "out_degree_tg"]
    elif metric == "out_degree":
        columns = ["tx_id", "in_degree_tg", "out_degree_tg"]
    elif metric == "pagerank":
        columns = ["tx_id", "pagerank_tg"]
    else: # metric == "harmonic"
        return None # Not implemented yet.
    tg_metric = load_metric_df("tg", metric, columns=columns)
    ag_rank = compute_rank("ag", metric).rename({"node_id" : "address_id", f"{metric}" : f"{metric}_ag"})
    x1 = tg_metric.join(tx_outputs, on="tx_id", how="left")
    x2 = x1.join(ag_rank, on="address_id", how="left")
    return x2.group_by("tx_id").agg(pl.col("rank").min()).join(ag_rank, on="rank", how="left").select("tx_id", "address_id")

def ug_to_ag(metric):
    """
    """
    assert metric in METRICS
    comp_map = load_comp_df().rename({"node_id": "address_id"})
    ag_rank = compute_rank("ag", metric).rename({"node_id" : "address_id", f"{metric}" : f"{metric}_ag"})
    x = ag_rank.join(comp_map, on="address_id", how="left")
    return (x.group_by("comp_id").agg(pl.col("rank").min()).join(ag_rank, on="rank", how="left").select("comp_id", "address_id"))

def atg_to_ag(metric):
    """
    """
    assert metric in METRICS
    # First half of the result is node_id mapped to itself (address -> address).
    res_1 = pl.DataFrame({'node_id' : range(0, NUM_UNIQUE_ADDR), 'address_id' : range(0, NUM_UNIQUE_ADDR)})
    # Second half of the result is transaction node_id mapped to address_id via tx_outputs.
    res_2 = tg_to_ag(metric).rename({"tx_id":"node_id"}).sort("node_id").with_columns(pl.col("node_id") + NUM_UNIQUE_ADDR)
    return pl.concat([res_1, res_2])

def pg_to_ag(metric):
    """
    """
    assert metric in METRICS
    pg_metric = load_metric_df("pg", metric).rename({"node_id":"payment_id"})
    pay_map = load_paymap_df()
    tx_outputs = load_txout_df()
    return (pg_metric.join(pay_map, on="payment_id", how="left")
            .join(tx_outputs, on=["tx_id", "output_id"], how="left")
            .select("payment_id", "address_id"))