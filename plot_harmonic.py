"""
Author: Matteo Loporchio
"""

import polars as pl
import matplotlib.pyplot as plt
import numpy as np
import sys
import plot_utils

NUM_BINS = 100
Y_MIN = 1
Y_MAX = 1e8

def plot_harmonic(df: pl.DataFrame, model: str, output_file: str):
    """
    Plot the distribution of the harmonic centrality.
    """
    plot_title = f"{model.upper()} harm. cent."
    color = plot_utils.get_color(model)
    yfmt = plot_utils.ScalarFormatterForceFormat()
    yfmt.set_powerlimits((0,0))
    data = df['harmonic']
    plt.figure(figsize=plot_utils.DEFAULT_FIGURE_SIZE)
    plt.hist(data, bins=NUM_BINS, color=color)
    plt.title(plot_title)
    plt.xlabel("harm. cent.")
    plt.ylabel("frequency")
    plt.yscale('log')
    plt.gca().xaxis.set_major_formatter(yfmt)
    plt.xticks(ha='left', rotation=90)
    plt.ylim(bottom = Y_MIN, top = Y_MAX)
    plt.yticks([1e1, 1e3, 1e5, 1e7])
    plt.grid(linestyle='--', linewidth=0.5)
    plt.gca().xaxis.get_offset_text().set_fontsize(plot_utils.DEFAULT_OFFSET_FONT_SIZE)
    plt.savefig(output_file, format='pdf', bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(f"Usage: python {sys.argv[0]} <input_file> <output_file> <model>")
        sys.exit(1)
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    model = sys.argv[3]
    df = pl.read_parquet(input_file)
    df.columns = ['node_id', 'harmonic']
    plot_harmonic(df, model, output_file)