"""One plot style for all EDA notebooks: colours, font sizes and where figures are saved.

Use it in a notebook (notebooks run in notebooks/<folder>/):

    import sys
    sys.path.insert(0, "../..")
    from src.plot_style import BLUE, ORANGE, GREY, save_figure

Importing the module sets the matplotlib style. Every figure is WIDTH inches wide,
so text has the same size in all figures.
"""
from pathlib import Path

import matplotlib.pyplot as plt
from cycler import cycler

# Blue: solar generation, the main series. Orange: weather, or a highlighted value.
# Greys: comparison and background.
BLUE, LIGHT_BLUE = "#2a78d6", "#7fb0e8"
ORANGE = "#eb6834"
GREY, DARK_GREY = "#c3c2b7", "#8a897f"
GRID = "#e1e0d9"
WIDTH = 10

plt.rcParams.update({
    "figure.dpi": 110, "savefig.dpi": 160, "savefig.bbox": "tight",
    "font.size": 10, "axes.titlesize": 11, "axes.labelsize": 10, "figure.titlesize": 12,
    "xtick.labelsize": 9, "ytick.labelsize": 9, "legend.fontsize": 9, "legend.frameon": False,
    "axes.grid": True, "grid.color": GRID, "axes.spines.top": False, "axes.spines.right": False,
    "axes.prop_cycle": cycler(color=[BLUE, ORANGE, DARK_GREY, GREY]),
})

FIGURES = Path(__file__).resolve().parents[1] / "figures" / "eda"


def save_figure(fig, name, details=False):
    """Save to figures/eda/, or to figures/eda/sources/ for the detail figures of the source notebooks."""
    folder = FIGURES / "sources" if details else FIGURES
    folder.mkdir(parents=True, exist_ok=True)
    fig.savefig(folder / f"{name}.png")
