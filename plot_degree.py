"""
Author: Matteo Loporchio
"""

import polars as pl
import matplotlib.pyplot as plt
import numpy as np
import sys
import plot_utils

Y_MAX = 1e9

def plot_in_degree_distribution(df: pl.DataFrame, model: str, output_file: str):
    """
    Plot the in-degree distribution of a graph.
    """
    plot_title = f"{model.upper()} in-degree"
    color = plot_utils.get_color(model)
    data = df['in_degree'].value_counts().sort('in_degree')
    plt.figure(figsize=plot_utils.DEFAULT_FIGURE_SIZE)
    plt.scatter(data['in_degree'], data['count'], marker='o', color=color, rasterized=True)
    plt.title(plot_title)
    plt.xlabel('in-degree')
    plt.ylabel('frequency')
    plt.xscale('symlog')
    plt.yscale('log')
    plt.xticks(ha='left', rotation=90)
    tick_labels = plt.xticks()[1]
    tick_labels[0].set_horizontalalignment('center')
    plt.ylim(top = Y_MAX)
    plt.grid(linestyle='--', linewidth=0.5)
    #plot_utils.set_font_size(plt.gca())
    plt.savefig(output_file, format='pdf', bbox_inches='tight')
    plt.close()

def plot_out_degree_distribution(df: pl.DataFrame, model: str, output_file: str):
    """
    Plot the out-degree distribution of a graph.
    """
    plot_title = f"{model.upper()} out-degree"
    color = plot_utils.get_color(model)
    data = df['out_degree'].value_counts().sort('out_degree')
    plt.figure(figsize=plot_utils.DEFAULT_FIGURE_SIZE)
    plt.scatter(data['out_degree'], data['count'], marker='o', color=color, rasterized=True)
    plt.title(plot_title)
    plt.xlabel("out-degree")
    plt.ylabel("frequency")
    plt.xscale('symlog')
    plt.yscale('log')
    plt.xticks(ha='left', rotation=90)
    tick_labels = plt.xticks()[1]
    tick_labels[0].set_horizontalalignment('center')
    plt.ylim(top = Y_MAX)
    plt.grid(linestyle='--', linewidth=0.5)
    #plot_utils.set_font_size(plt.gca())
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
    plot_in_degree_distribution(df, model, output_file + "_in.pdf")
    plot_out_degree_distribution(df, model, output_file + "_out.pdf")