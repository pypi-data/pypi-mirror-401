from __future__ import annotations

import math
from pathlib import Path
from typing import Any

import h5py
import matplotlib.pyplot as plt
from networkx import DiGraph, Graph, draw_networkx_edges, draw_networkx_labels, draw_networkx_nodes, nx_agraph
from pydantic import BaseModel, Field

Edge = tuple[str, str]


class TopologyPlot(BaseModel):
    """Load topology from an HDF5 file and plot it."""

    h5_path: Path = Field(..., description="Path to the results .h5 file containing /topology")

    # optional: cache the loaded representation so we don't reread the file repeatedly
    _graph_representation: dict[str, Any] | None = None

    def _load_topology(self) -> dict[str, list]:
        """Read /topology/nodes and /topology/edges from the HDF5."""
        with h5py.File(self.h5_path, "r") as f:
            if "topology" not in f:
                raise KeyError(f"Missing group '/topology' in {self.h5_path}")

            topo = f["topology"]
            if "nodes" not in topo or "edges" not in topo:
                raise KeyError(f"Missing datasets '/topology/nodes' or '/topology/edges' in {self.h5_path}")

            nodes_raw = topo["nodes"][()]
            edges_raw = topo["edges"][()]

        def _to_str(x) -> str:
            return x.decode("utf-8") if isinstance(x, (bytes, bytearray)) else str(x)

        nodes = [_to_str(n) for n in nodes_raw]

        edges: list[Edge] = []
        # edges_raw should be shape (N, 2); handle empty safely
        if getattr(edges_raw, "shape", None) is not None and len(edges_raw) > 0:
            for u, v in edges_raw:
                edges.append((_to_str(u), _to_str(v)))

        return {"nodes": nodes, "edges": edges}

    @property
    def graph_representation(self) -> dict[str, list]:
        """Lazy-load and cache."""
        if self._graph_representation is None:
            self._graph_representation = self._load_topology()
        return self._graph_representation  # type: ignore[return-value]

    def build_graph(self) -> DiGraph:
        rep = self.graph_representation
        graph = DiGraph()
        graph.add_nodes_from(rep["nodes"])
        graph.add_edges_from(rep["edges"])
        return graph

    def _layout(
        self,
        graph: DiGraph,
        *,
        use_graphviz: bool = True,
        grid_dx: float = 1.0,
        grid_dy: float = 1.0,
        sort_nodes: bool = True,
    ):
        def _grid_layout(graph: Graph, *, dx: float, dy: float, sort_nodes: bool):
            nodes = list(graph.nodes())
            if sort_nodes:
                nodes = sorted(nodes, key=str)

            n = len(nodes)
            if n == 0:
                return {}

            cols = math.ceil(math.sqrt(n))
            return {node: (dx * (i % cols), -dy * (i // cols)) for i, node in enumerate(nodes)}

        if use_graphviz:
            # keep your current graphviz behavior if you have it
            try:
                return nx_agraph.graphviz_layout(graph, prog="dot")
            except Exception:
                # If graphviz/pygraphviz isn't installed, fall back to grid
                return _grid_layout(graph, dx=grid_dx, dy=grid_dy, sort_nodes=sort_nodes)

        # non-graphviz layout: equally spaced grid
        return _grid_layout(graph, dx=grid_dx, dy=grid_dy, sort_nodes=sort_nodes)

    def save_topology_plot(
        self,
        pdf_path: str | Path,
        *,
        use_graphviz: bool = True,
        figsize: tuple[float, float] = (10, 6),
    ) -> tuple[DiGraph, str]:
        graph = self.build_graph()
        pos = self._layout(graph, use_graphviz=use_graphviz, grid_dx=2.0, grid_dy=2.0)

        # label offset: right (+dx) and up (+dy)
        dx, dy = 0.0, 0.3
        label_pos = {n: (x + dx, y + dy) for n, (x, y) in pos.items()}

        fig = plt.figure(figsize=figsize)
        ax = plt.gca()
        ax.set_axis_off()

        # edges (transparent grey-ish)
        draw_networkx_edges(
            graph,
            pos,
            ax=ax,
            arrows=True,
            arrowsize=15,
            edge_color="0.4",
            alpha=0.25,
            width=1.5,
        )

        draw_networkx_nodes(
            graph,
            pos,
            ax=ax,
            node_size=500,
            node_color="0.85",
            edgecolors="0.4",
            linewidths=1.0,
        )

        # labels (offset above-right)
        draw_networkx_labels(
            graph,
            label_pos,
            ax=ax,
            font_size=8,
            font_color="black",
            horizontalalignment="center",
            verticalalignment="bottom",
        )

        plt.tight_layout()

        pdf_path = Path(pdf_path)
        pdf_path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(pdf_path, format="pdf", bbox_inches="tight")
        plt.close(fig)

        return graph, str(pdf_path)

    def plot_into(self, ax: plt.Axes, *, use_graphviz: bool = True) -> DiGraph:
        graph = self.build_graph()
        pos = self._layout(graph, use_graphviz=use_graphviz)

        # label directly above nodes
        dx, dy = 0.0, 0.3
        label_pos = {n: (x + dx, y + dy) for n, (x, y) in pos.items()}

        ax.clear()
        ax.set_axis_off()

        draw_networkx_edges(
            graph,
            pos,
            ax=ax,
            arrows=True,
            arrowsize=15,
            edge_color="0.4",
            alpha=0.25,
            width=1.5,
        )

        draw_networkx_nodes(
            graph,
            pos,
            ax=ax,
            node_size=500,
            node_color="0.85",
            edgecolors="0.4",
            linewidths=1.0,
        )

        draw_networkx_labels(
            graph,
            label_pos,
            ax=ax,
            font_size=9,
            font_color="black",
            horizontalalignment="center",
            verticalalignment="bottom",
        )

        # --- ONLY FIX HEIGHT (top labels clipped), keep width as-is ---
        if pos:
            ys = [p[1] for p in pos.values()]
            lys = [p[1] for p in label_pos.values()]  # include labels above nodes

            ymin = min(ys + lys)
            ymax = max(ys + lys)

            yspan = (ymax - ymin) or 1.0
            pad_y = 0.20 * yspan  # bump to 0.30 if needed

            ax.set_ylim(ymin - pad_y, ymax + pad_y)

        # IMPORTANT: don't force equal aspect (shrinks in subplots)
        ax.set_aspect("auto")

        return graph


if __name__ == "__main__":
    topo = TopologyPlot(
        h5_path="C:/Git/eta-incerto/examples/hp_comparison/results/stochastic_expected_with_invest_opex.h5"
    )
    pdf_path = Path("C:/Git/eta-incerto/examples/hp_comparison/plots") / "stochastic_expected_with_invest_opex.pdf"
    topo.save_topology_plot(pdf_path)
