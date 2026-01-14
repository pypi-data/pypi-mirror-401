from __future__ import annotations

from dataclasses import dataclass

import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

A4_W, A4_H = 8.27, 11.69


def _off(ax: plt.Axes) -> None:
    ax.set_axis_off()


@dataclass
class SummaryAxes2Topo:
    ax_title: plt.Axes
    ax_topo_wo: plt.Axes
    ax_topo_w: plt.Axes
    ax_perf: list[plt.Axes]  # [Energy, Costs, Emissions]
    ax_footer: plt.Axes


def create_a4_template_two_topologies(
    title: str,
    subtitle: str = "",
    footer_left: str = "",
    footer_right: str = "",
) -> tuple[plt.Figure, SummaryAxes2Topo]:
    plt.rcParams.update(
        {
            "font.size": 10,
            "axes.titlesize": 11,
            "axes.labelsize": 10,
            "legend.fontsize": 9,
            "xtick.labelsize": 9,
            "ytick.labelsize": 9,
            "axes.grid": True,
            "grid.alpha": 0.3,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
        }
    )

    fig = plt.figure(figsize=(A4_W, A4_H))
    fig.subplots_adjust(left=0.06, right=0.07, top=0.0, bottom=0.06)

    # header | topo row (2 columns) | performance row (3 columns) | footer
    gs = GridSpec(
        nrows=10,
        ncols=6,
        figure=fig,
        height_ratios=[0.9, 0.15, 3.0, 0.2, 2.2, 0.2, 0.1, 0.1, 0.1, 0.55],
        hspace=0.20,
        wspace=0.20,
    )

    ax_title = fig.add_subplot(gs[0, :])
    ax_topo_wo = fig.add_subplot(gs[2, 0:3])
    ax_topo_w = fig.add_subplot(gs[2, 3:6])

    ax_p1 = fig.add_subplot(gs[4, 0:2])
    ax_p2 = fig.add_subplot(gs[4, 2:4])
    ax_p3 = fig.add_subplot(gs[4, 4:6])

    ax_footer = fig.add_subplot(gs[-1, :])

    _off(ax_title)
    _off(ax_footer)

    header = title if not subtitle else f"{title}\n{subtitle}"
    ax_title.text(0.5, 0.55, header, ha="center", va="center", fontsize=16, fontweight="bold")

    ax_footer.text(0.01, 0.5, footer_left, ha="left", va="center", fontsize=9)
    ax_footer.text(0.99, 0.5, footer_right, ha="right", va="center", fontsize=9)

    axes = SummaryAxes2Topo(
        ax_title=ax_title,
        ax_topo_wo=ax_topo_wo,
        ax_topo_w=ax_topo_w,
        ax_perf=[ax_p1, ax_p2, ax_p3],
        ax_footer=ax_footer,
    )
    return fig, axes
