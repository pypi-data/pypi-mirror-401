from pathlib import Path

import h5py
import matplotlib.pyplot as plt
import seaborn as sns
from numpy import (
    arange,
    array,
    hstack,
    max as npmax,
    min as npmin,
)
from pandas import DataFrame

from eta_incerto.config.config_plotting import ConfigPlotting
from eta_incerto.config.config_problem import ConfigProblem


class DoePlotter:
    """Simple plotter for DOE results saved in HDF5 (no normalization)."""

    def __init__(self, problem_config: ConfigProblem, h5_folder_path: str, h5_file: str):
        folder = Path(h5_folder_path)
        self.h5_file = folder / h5_file
        if not self.h5_file.exists():
            raise FileNotFoundError(f"HDF5 file not found: {self.h5_file}")

        self.df, self.var_names, self.obj_names = self._load_h5()

    def _load_h5(self):
        """Load DOE results from HDF5 into a DataFrame (no normalization)."""
        with h5py.File(self.h5_file, "r") as f:
            doe_x = f["doe/X"][:]
            doe_f = f["doe/F"][:]

            var_names = [n.decode() if isinstance(n, bytes) else str(n) for n in f["doe/variable_names"][:]]
            obj_names = [n.decode() if isinstance(n, bytes) else str(n) for n in f["doe/objective_names"][:]]

        loaded_df = DataFrame(hstack([doe_x, doe_f]), columns=var_names + obj_names)
        return loaded_df, var_names, obj_names

    @staticmethod
    def reduce_ticks(ax, xdata=None, ydata=None):
        """Keep only npmin, mid, and npmax ticks on axes, based on dataset range."""
        if xdata is not None and len(xdata) >= 2:
            xmin, xmax = npmin(xdata), npmax(xdata)
            xmid = (xmin + xmax) / 2
            ax.set_xticks([xmin, xmid, xmax])

        if ydata is not None and len(ydata) >= 2:
            ymin, ymax = npmin(ydata), npmax(ydata)
            ymid = (ymin + ymax) / 2
            ax.set_yticks([ymin, ymid, ymax])

    @staticmethod
    def keep_x_y_axes(ax):
        """Keep only bottom and left spines visible."""
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["bottom"].set_visible(True)
        ax.spines["left"].set_visible(True)

    def plot(self, config: ConfigPlotting, outpath: Path):
        """Plot DOE scatter plots as configured in config.subplots."""
        plt.rcParams.update(config.rcparams)
        nplots = len(config.subplots)
        nrows = (nplots + 1) // 2
        fig, axs = plt.subplots(nrows, 2, figsize=(config.fig_w_in, config.fig_h_in), constrained_layout=True)
        axs = axs.flatten()

        for conf in config.subplots:
            x, y, idx = conf.x, conf.y, conf.subplot
            ax = axs[idx]

            cvar = getattr(conf, "color", None)
            if cvar and cvar in self.df.columns:
                sc = ax.scatter(self.df[x], self.df[y], c=self.df[cvar], cmap="plasma", edgecolors="k", s=20)
                fig.colorbar(sc, ax=ax, label=str(cvar))
            else:
                ax.scatter(self.df[x], self.df[y], s=20, c="steelblue", alpha=0.7)

            ax.set_xlabel(conf.xlabel or x)
            ax.set_ylabel(conf.ylabel or y, rotation=0, labelpad=5, ha="right", va="bottom")
            ax.set_title(conf.title or None)

            self.reduce_ticks(ax, self.df[x].to_numpy(), self.df[y].to_numpy())
            self.keep_x_y_axes(ax)
            ax.grid(False)

        plt.savefig(outpath, format="pdf", bbox_inches="tight")
        plt.close(fig)

    def plot_sobol_indices(self, config: ConfigPlotting, outpath: Path):
        """
        Plot first-order (S1), total-order (ST), and second-order (S2) Sobol indices
        for all available metric groups under h5 file section /doe/sobol.

        Parameters
        ----------
        outpath : Path
            If provided, saves a multi-page PDF (one page per Sobol metric group);
            otherwise shows plots interactively.
        """
        with h5py.File(self.h5_file, "r") as f:
            sobol_root = f["doe/sobol"]
            metrics = list(sobol_root.keys())
            var_names = config.dist_names

            n_metrics = len(metrics)
            fig, axs = plt.subplots(n_metrics, 2, figsize=(10, 4 * n_metrics), constrained_layout=True)

            # Handle case with only one metric
            if n_metrics == 1:
                axs = array([axs])

            for i, metric in enumerate(metrics):
                base = sobol_root[metric]
                S1 = base["S1"][:]  # noqa N806
                ST = base["ST"][:]  # noqa N806
                S2 = base["S2"][:]  # noqa N806

                # --- Bar plot for S1 and ST
                ax = axs[i, 0]
                width = 0.35
                x = arange(len(var_names))
                ax.bar(x - width / 2, S1, width, label="S1", color="tab:blue")
                ax.bar(x + width / 2, ST, width, label="ST", color="tab:orange")
                ax.set_xticks(x)
                ax.set_xticklabels(var_names, rotation=45, ha="right")
                ax.set_ylabel("Sobol index value")
                ax.set_title(f"S1 / ST ({metric})")
                ax.legend()

                # --- Heatmap for S2
                ax2 = axs[i, 1]
                sns.heatmap(
                    S2,
                    annot=True,
                    fmt=".2f",
                    xticklabels=var_names,
                    yticklabels=var_names,
                    cmap="coolwarm",
                    cbar_kws={"label": "S2"},
                    ax=ax2,
                )
                ax2.set_title(f"S2 ({metric})")

        plt.savefig(outpath, format="pdf", bbox_inches="tight")
        plt.close(fig)
