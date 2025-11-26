"""
Author: Matteo Loporchio
"""

import polars as pl
import matplotlib.pyplot as plt
import numpy as np
import sys
import plot_utils

NUM_BINS = 100

def plot_pagerank(df: pl.DataFrame, model: str, output_file: str):
    """
    Plot the distribution of the PageRank centrality measure.
    """
    plot_title = f"{model.upper()} PageRank"
    color = plot_utils.get_color(model)
    data = df['pagerank']
    plt.figure(figsize=plot_utils.DEFAULT_FIGURE_SIZE)
    plt.hist(data, bins=NUM_BINS, color=color)
    plt.title(plot_title)
    plt.xlabel("PageRank")
    plt.ylabel("frequency")
    plt.yscale('log')
    plt.gca().ticklabel_format(axis='x', style='sci', scilimits=(0, 0))
    plt.grid(linestyle='--', linewidth=0.5)
    plot_utils.set_font_size(plt.gca())
    plt.savefig(output_file, format='pdf', bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(f"Usage: python {sys.argv[0]} <input_file> <output_file> <model>")
        sys.exit(1)
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    model = sys.argv[3]
    df = pl.read_csv(input_file, separator="\t", null_values=["nan", "-nan"])
    plot_pagerank(df, model, output_file)