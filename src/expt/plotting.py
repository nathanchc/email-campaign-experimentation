"""Shared chart style so every notebook looks the same.

Colours come from a colour-blind-checked palette: one fixed colour per
experiment arm, used consistently across notebooks.
"""
from __future__ import annotations

import matplotlib.pyplot as plt

INK = "#0b0b0b"
INK_2 = "#52514e"
SURFACE = "#fcfcfb"
GRID = "#e4e3df"
AXIS = "#c9c8c3"
BAND = "#f0efec"

ARM_COLORS = {"control": "#1baf7a", "mens": "#2a78d6", "womens": "#eb6834"}
ARM_LABELS = {"control": "No e-mail", "mens": "Men's e-mail", "womens": "Women's e-mail"}
SERIES = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4"]


def new_figure(width: float = 8, height: float = 4.5, ncols: int = 1):
    fig, axes = plt.subplots(1, ncols, figsize=(width, height), facecolor=SURFACE)
    for ax in (axes if ncols > 1 else [axes]):
        ax.set_facecolor(SURFACE)
    return fig, axes


def style_axes(ax, title: str | None = None, xlabel: str | None = None, ylabel: str | None = None, grid: str = "y"):
    if title:
        ax.set_title(title, loc="left", color=INK, fontsize=11)
    if xlabel:
        ax.set_xlabel(xlabel, color=INK_2)
    if ylabel:
        ax.set_ylabel(ylabel, color=INK_2)
    if grid:
        ax.grid(axis=grid, color=GRID, linewidth=0.8)
        ax.set_axisbelow(True)
    ax.tick_params(colors=INK_2)
    for side in ["top", "right"]:
        ax.spines[side].set_visible(False)
    for side in ["left", "bottom"]:
        ax.spines[side].set_color(AXIS)
    return ax
