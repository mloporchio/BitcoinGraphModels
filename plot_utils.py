"""
This script contains utility functions for plotting the results of the experiments.

Author: Matteo Loporchio
"""

import matplotlib.pyplot as plt
import os
from matplotlib import font_manager
from matplotlib.ticker import ScalarFormatter

DEFAULT_FONT_SIZE = 22
DEFAULT_OFFSET_FONT_SIZE = 20
DEFAULT_FIGURE_SIZE = (4, 4)

# Set default font
DEFAULT_FONT_PATH = 'fonts/texgyreheros-regular.otf'
if os.path.exists(DEFAULT_FONT_PATH):
    font_manager.fontManager.addfont(DEFAULT_FONT_PATH)
    prop = font_manager.FontProperties(fname=DEFAULT_FONT_PATH)
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = prop.get_name()

plt.rcParams.update({'font.size': DEFAULT_FONT_SIZE})
plt.rcParams.update({'axes.titlesize': DEFAULT_FONT_SIZE})
plt.rcParams.update

COLORS = {
    "ag" : "#377eb8",
    "tg" : "#e41a1c",
    "ug" : "#4daf4a",
    "atg" : "#984ea3",
    "pg" : "#ff7f00"
} # SOURCE: https://colorbrewer2.org/#type=qualitative&scheme=Set1&n=5

def get_color(model):
    if model in COLORS.keys():
        return COLORS[model]
    else:
        raise ValueError(f"Unknown model: {model}")

class ScalarFormatterForceFormat(ScalarFormatter):
    def _set_format(self):  # Override function that finds format to use.
        self.format = "%1.2f"  # Give format here

def set_font_size(ax, font_size=DEFAULT_FONT_SIZE):
    for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] + ax.get_xticklabels() + ax.get_yticklabels()):
        item.set_fontsize(font_size)