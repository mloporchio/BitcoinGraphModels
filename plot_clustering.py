"""

"""

import polars as pl
import matplotlib.pyplot as plt
import numpy as np
import sys

FONT_SIZE = 14
FIGURE_SIZE = (4, 4)
STEP = 0.01  # Step size for histogram bins

def set_font_size(ax, font_size):
    for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] + ax.get_xticklabels() + ax.get_yticklabels()):
        item.set_fontsize(font_size)

def plot_clustering(df: pl.DataFrame, output_file: str, plot_title: str):
    """
    Plot the distribution of the clustering coefficient.
    """
    data = df['clustering'].drop_nulls().cast(pl.Float64)
    plt.figure(figsize=FIGURE_SIZE)
    plt.hist(data, bins=np.arange(0, 1 + STEP, STEP), color="blue")
    plt.title(plot_title)
    plt.xlabel("Clustering coefficient")
    plt.ylabel("Frequency")
    plt.yscale('log')
    plt.grid(linestyle='--', linewidth=0.5)
    set_font_size(plt.gca(), FONT_SIZE)
    plt.savefig(output_file, format='pdf', bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(f"Usage: python {sys.argv[0]} <input_file> <output_file> <model_name>")
        sys.exit(1)
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    plot_title = sys.argv[3]
    df = pl.read_csv(input_file, separator="\t", null_values=["nan", "-nan"])
    plot_clustering(df, output_file, plot_title)