import polars as pl
import matplotlib.pyplot as plt
import numpy as np
import sys

FONT_SIZE = 14

def set_font_size(ax, font_size):
    for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] + ax.get_xticklabels() + ax.get_yticklabels()):
        item.set_fontsize(font_size)

def plot_in_degree_distribution(df: pl.DataFrame, output_file: str, plot_title: str):
    """
    Plot the in-degree distribution of a graph.
    """
    data = df['in_degree'].value_counts().sort('in_degree')
    plt.figure(figsize=(4, 4))
    plt.scatter(data['in_degree'], data['count'], color="blue", rasterized=True)
    plt.title(plot_title)
    plt.xlabel("In-Degree")
    plt.ylabel("Frequency")
    plt.xscale('symlog')
    plt.yscale('log')
    plt.grid(linestyle='--', linewidth=0.5)
    set_font_size(plt.gca(), FONT_SIZE)
    plt.savefig(output_file, format='pdf', bbox_inches='tight')
    plt.close()

def plot_out_degree_distribution(df: pl.DataFrame, output_file: str, plot_title: str):
    """
    Plot the out-degree distribution of a graph.
    """
    data = df['out_degree'].value_counts().sort('out_degree')
    plt.figure(figsize=(4, 4))
    plt.scatter(data['out_degree'], data['count'], color="blue", rasterized=True)
    plt.title(plot_title)
    plt.xlabel("Out-Degree")
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
    plot_in_degree_distribution(df, output_file + "_in.pdf", f"{model_name} In-Degree")
    plot_out_degree_distribution(df, output_file + "_out.pdf", f"{model_name} Out-Degree")