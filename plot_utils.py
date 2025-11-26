"""
Author: Matteo Loporchio
"""

DEFAULT_FONT_SIZE = 14
DEFAULT_FIGURE_SIZE = (4,4)
COLORS = {
    "ag" : "#377eb8",
    "tg" : "#e41a1c",
    "ug" : "#4daf4a",
    "atg" : "#984ea3",
    "pg" : "#ff7f00"
} # SOURCE: https://colorbrewer2.org/#type=qualitative&scheme=Set1&n=5

def set_font_size(ax, font_size=DEFAULT_FONT_SIZE):
    for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] + ax.get_xticklabels() + ax.get_yticklabels()):
        item.set_fontsize(font_size)

def get_color(model):
    if model in COLORS.keys():
        return COLORS[model]
    else:
        raise ValueError(f"Unknown model: {model}")