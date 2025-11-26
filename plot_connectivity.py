"""
Author: Matteo Loporchio
"""

import polars as pl
import matplotlib.pyplot as plt
import numpy as np
import sys
import plot_utils

def plot_weak(df: pl.DataFrame, model: str, output_file: str):
    """
    Plot the distribution of the weakly connected component sizes.
    """
    plot_title = f"{model.upper()} WCC size"
    color = plot_utils.get_color(model)
    data = df['wcc_id'].value_counts(name='comp_size')['comp_size'].value_counts().sort('comp_size')
    plt.figure(figsize=plot_utils.DEFAULT_FIGURE_SIZE)
    plt.scatter(data['comp_size'], data['count'], color=color, rasterized=True)
    plt.title(plot_title)
    plt.xlabel("WCC size")
    plt.ylabel("frequency")
    plt.xscale('symlog')
    plt.yscale('log')
    plt.grid(linestyle='--', linewidth=0.5)
    plot_utils.set_font_size(plt.gca())
    plt.savefig(output_file, format='pdf', bbox_inches='tight')
    plt.close()

def plot_strong(df: pl.DataFrame, model: str, output_file: str):
    """
    Plot the distribution of the strongly connected component sizes.
    """
    plot_title = f"{model.upper()} SCC size"
    color = plot_utils.get_color(model)
    data = df['scc_id'].value_counts(name='comp_size')['comp_size'].value_counts().sort('comp_size')
    plt.figure(figsize=plot_utils.DEFAULT_FIGURE_SIZE)
    plt.scatter(data['comp_size'], data['count'], color=color, rasterized=True)
    plt.title(plot_title)
    plt.xlabel("SCC size")
    plt.ylabel("frequency")
    plt.xscale('symlog')
    plt.yscale('log')
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
    df = pl.read_csv(input_file, separator="\t")
    plot_weak(df, model, output_file + "_weak.pdf")
    plot_strong(df, model, output_file + "_strong.pdf")