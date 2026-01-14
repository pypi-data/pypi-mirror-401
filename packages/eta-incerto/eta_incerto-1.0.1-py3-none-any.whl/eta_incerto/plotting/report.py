from __future__ import annotations

import datetime as dt
from pathlib import Path

import h5py
import matplotlib.pyplot as plt

from eta_incerto.plotting.summary_template import create_a4_template_two_topologies


class A4SummaryReport:
    def __init__(
        self,
        *,
        perf,
        topo_wo,
        topo_w,
        path_wo_invest: Path,
        path_w_invest: Path,
        title: str,
        subtitle: str = "",
        footer_right: str = "Michael Frank",
        style: dict | None = None,
    ) -> None:
        self.perf = perf
        self.topo_wo = topo_wo
        self.topo_w = topo_w
        self.title = title
        self.subtitle = subtitle
        self.footer_right = footer_right
        self.style = style or {}
        self.path_wo_invest = path_wo_invest
        self.path_w_invest = path_w_invest

    def _read_time_tag(self, h5_path: Path) -> str | None:
        try:
            with h5py.File(h5_path, "r") as f:
                if "meta" not in f or "time_tag" not in f["meta"]:
                    return None
                raw = f["meta"]["time_tag"][()]
        except OSError:
            return None

        return raw.decode("utf-8") if isinstance(raw, (bytes, bytearray)) else str(raw)

    def render(self, *, footer_left: str | None = None):
        # Example: if your report has two source files:
        # self.path_wo_invest and self.path_w_invest (adjust names accordingly)
        tag_wo = self._read_time_tag(self.path_wo_invest)
        tag_w = self._read_time_tag(self.path_w_invest)

        if footer_left is None:
            if tag_wo and tag_w:
                footer_left = f"Run: wo={tag_wo} | w={tag_w}"
            elif tag_wo or tag_w:
                footer_left = f"Run: {tag_wo or tag_w}"
            else:
                footer_left = f"Run: {dt.datetime.now(tz='Europe/Berlin').strftime('%Y%m%d_%H%M%S_%z')}"

        fig, ax = create_a4_template_two_topologies(
            title=self.title,
            subtitle=self.subtitle,
            footer_left=footer_left,
            footer_right=self.footer_right,
        )

        # Titles for the topology panes
        ax.ax_topo_wo.set_title("Topology (without invest)", pad=10)
        ax.ax_topo_w.set_title("Topology (with invest)", pad=10)

        # Draw into axes (requires your plot_into refactor)
        self.topo_wo.plot_into(ax.ax_topo_wo, use_graphviz=True)
        self.topo_w.plot_into(ax.ax_topo_w, use_graphviz=True)
        self.perf.plot_into(ax.ax_perf)

        return fig, ax

    def save(self, out_pdf: str | Path, *, footer_left: str | None = None) -> Path:
        out_pdf = Path(out_pdf)
        fig, _ = self.render(footer_left=footer_left)
        out_pdf.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(out_pdf, format="pdf")
        plt.close(fig)
        return out_pdf
