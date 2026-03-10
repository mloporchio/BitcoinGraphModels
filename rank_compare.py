"""
Author: Matteo Loporchio
"""

import polars as pl
import utils
import sys

def compute_rank(model, metric):
    assert (model in utils.MODELS) and (metric in utils.METRICS)
    metric_df = utils.load_metric_df(model, metric)
    ranked_df = metric_df.select("node_id", metric).sort(metric, descending=True).with_row_index("rank")
    return ranked_df

def tg_to_ag(metric):
    assert metric in utils.METRICS
    tx_outputs = utils.load_txout_df() # Read the transaction output list.
    columns = None
    if metric == "in_degree":
        columns = ["tx_id", "in_degree_tg", "out_degree_tg"]
    elif metric == "out_degree":
        columns = ["tx_id", "in_degree_tg", "out_degree_tg"]
    elif metric == "pagerank":
        columns = ["tx_id", "pagerank_tg"]
    else:
        columns = ["tx_id", "harmonic_tg"]
    tg_metric = utils.load_metric_df("tg", metric, columns=columns)
    ag_rank = compute_rank("ag", metric).rename({"node_id" : "address_id", f"{metric}" : f"{metric}_ag"})
    x1 = tg_metric.join(tx_outputs, on="tx_id", how="left")
    x2 = x1.join(ag_rank, on="address_id", how="left")
    return (x2.group_by("tx_id").agg(pl.col("rank").min())
            .join(ag_rank, on="rank", how="left")
            .select("tx_id", "address_id"))

def ug_to_ag(metric):
    """
    """
    assert metric in utils.METRICS
    comp_map = utils.load_map_comp(columns=["address_id", "comp_id"])
    ag_rank = compute_rank("ag", metric).rename({"node_id" : "address_id", f"{metric}" : f"{metric}_ag"})
    x = ag_rank.join(comp_map, on="address_id", how="left")
    return (x.group_by("comp_id").agg(pl.col("rank").min())
            .join(ag_rank, on="rank", how="left")
            .select("comp_id", "address_id"))

def atg_to_ag(metric):
    """
    """
    assert metric in utils.METRICS
    # First half of the result is node_id mapped to itself (address -> address).
    address_id_space = range(0, utils.NUM_UNIQUE_ADDR)
    res_1 = pl.DataFrame({'node_id' : address_id_space, 'address_id' : address_id_space})
    # Second half of the result is transaction node_id mapped to address_id via tx_outputs.
    res_2 = (tg_to_ag(metric).rename({"tx_id":"node_id"})
             .sort("node_id").with_columns(pl.col("node_id") + utils.NUM_UNIQUE_ADDR))
    return pl.concat([res_1, res_2])

def pg_to_ag(metric):
    """
    """
    assert metric in utils.METRICS
    pg_metric = utils.load_metric_df("pg", metric).select("node_id", metric).rename({"node_id":"payment_id"})
    pay_map = utils.load_map_payments()
    tx_outputs = utils.load_txout_df()
    result = (pg_metric.join(pay_map, on="payment_id", how="left")
              .join(tx_outputs, on=["tx_id", "output_id"], how="left")
              .select("payment_id", "address_id"))
    return result

def rank_compare(model_src, model_dst, metric):
    assert (model_src in utils.MODELS) and (model_dst in utils.MODELS) and (metric in utils.METRICS)
    if model_src == "tg" and model_dst == "ag":
        return tg_to_ag(metric)
    elif model_src == "ug" and model_dst == "ag":
        return ug_to_ag(metric)
    elif model_src == "atg" and model_dst == "ag":
        return atg_to_ag(metric)
    elif model_src == "pg" and model_dst == "ag":
        return pg_to_ag(metric)
    else:
        raise NotImplementedError(f"Rank comparison from {model_src} to {model_dst} not implemented.")
