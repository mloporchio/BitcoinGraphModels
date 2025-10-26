import polars as pl
import matplotlib.pyplot as plt
import numpy as np
import sys

FONT_SIZE = 14
FIGURE_SIZE = (4, 4)

def set_font_size(ax, font_size):
    for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] + ax.get_xticklabels() + ax.get_yticklabels()):
        item.set_fontsize(font_size)

def plot_weak(df: pl.DataFrame, output_file: str, plot_title: str):
    """
    Plot the distribution of the weakly connected component sizes.
    """
    data = df['wcc_id'].value_counts(name='comp_size')['comp_size'].value_counts().sort('comp_size')
    plt.figure(figsize=FIGURE_SIZE)
    plt.scatter(data['comp_size'], data['count'], color="blue", rasterized=True)
    plt.title(plot_title)
    plt.xlabel("WCC size")
    plt.ylabel("Frequency")
    plt.xscale('symlog')
    plt.yscale('log')
    plt.grid(linestyle='--', linewidth=0.5)
    set_font_size(plt.gca(), FONT_SIZE)
    plt.savefig(output_file, format='pdf', bbox_inches='tight')
    plt.close()

def plot_strong(df: pl.DataFrame, output_file: str, plot_title: str):
    """
    Plot the distribution of the strongly connected component sizes.
    """
    data = df['scc_id'].value_counts(name='comp_size')['comp_size'].value_counts().sort('comp_size')
    plt.figure(figsize=FIGURE_SIZE)
    plt.scatter(data['comp_size'], data['count'], color="blue", rasterized=True)
    plt.title(plot_title)
    plt.xlabel("SCC size")
    plt.ylabel("Frequency")
    plt.xscale('symlog')
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
    model_name = sys.argv[3]
    df = pl.read_csv(input_file, separator="\t")
    plot_weak(df, output_file + "_weak.pdf", f"{model_name} WCC")
    plot_strong(df, output_file + "_strong.pdf", f"{model_name} SCC")