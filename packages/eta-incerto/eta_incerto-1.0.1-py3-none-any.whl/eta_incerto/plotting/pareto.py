from pathlib import Path

import h5py
import matplotlib.pyplot as plt
from numpy import (
    array,
    hstack,
    inf,
    max as npmax,
    min as npmin,
    ndarray,
)
from pandas import DataFrame

from eta_incerto.config.config_plotting import ConfigPlotting
from eta_incerto.config.config_problem import ConfigProblem


class ParetoPlotter:
    def __init__(self, problem_config: ConfigProblem, h5_folder_path: str, h5_file: str):
        folder = Path(h5_folder_path)
        self.h5_file = folder / h5_file
        if not self.h5_file.exists():
            raise FileNotFoundError(f"HDF5 file not found: {self.h5_file}")

        self.df, self.var_names, self.obj_names = self._load_h5(problem_config)

    def _load_h5(self, config) -> DataFrame:
        """Load Pareto results from HDF5 into a DataFrame."""
        with h5py.File(self.h5_file, "r") as f:
            pareto_x = f["pareto/X"][:]
            pareto_f = f["pareto/F"][:]

            obj_min = array(config.obj_min, dtype=float)
            obj_max = array(config.obj_max, dtype=float)

            pareto_f = pareto_f * (obj_max - obj_min) + obj_min

            # Variable and objective names
            var_names = [n.decode() if isinstance(n, bytes) else str(n) for n in f["pareto/variable_names"][:]]
            obj_names = [n.decode() if isinstance(n, bytes) else str(n) for n in f["pareto/objective_names"][:]]

        # Build dataframe
        pareto_df = DataFrame(hstack([pareto_x, pareto_f]), columns=var_names + obj_names)
        return pareto_df, var_names, obj_names

    @staticmethod
    def reduce_ticks(ax, xdata=None, ydata=None):
        """Keep only min, mid, and max ticks on axes, based on full dataset."""
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
        """Keep only bottom and left spines, remove top and right."""
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["bottom"].set_visible(True)
        ax.spines["left"].set_visible(True)

    def remove_axes(self, fig, axs, indices):
        """Remove subplot axes by index (e.g., [1, 3])."""
        for idx in indices:
            if idx < len(axs):
                fig.delaxes(axs[idx])

    @staticmethod
    def pareto_front(points: ndarray) -> ndarray:
        """Compute 2D Pareto front (assuming minimization)."""
        points = points[points[:, 0].argsort()]  # sort by first objective
        pareto = []
        best_y = inf
        for x, y in points:
            if y < best_y:  # strictly better in second objective
                pareto.append((x, y))
                best_y = y
        return array(pareto)

    def plot(self, config: ConfigPlotting, outpath):
        plt.rcParams.update(config.rcparams)
        nplots = len(config.subplots)
        nrows = (nplots + 1) // 2
        fig, axs = plt.subplots(nrows, 2, figsize=(config.fig_w_in, config.fig_h_in), constrained_layout=True)
        axs = axs.flatten()

        for conf in config.subplots:
            x, y, idx = conf.x, conf.y, conf.subplot
            ax = axs[idx]

            if getattr(conf, "type", "line") == "scatter":
                cvar = getattr(conf, "color", None)
                cvar_label = getattr(conf, "color_label", None)
                if cvar is None or cvar not in self.df.columns:
                    raise ValueError(f"Color variable '{cvar}' not found in dataframe")

                sc = ax.scatter(self.df[x], self.df[y], c=self.df[cvar], cmap="plasma", edgecolors="k", s=20)
                fig.colorbar(sc, ax=ax, label=cvar_label)

            else:
                pts = self.df[[x, y]].to_numpy()
                pareto_pts = self.pareto_front(pts)

                # scatter all solutions
                ax.scatter(pts[:, 0], pts[:, 1], s=5, c="grey", alpha=0.5)
                # plot Pareto frontier
                ax.plot(pareto_pts[:, 0], pareto_pts[:, 1], "-o", c="black", markersize=3, linewidth=1)
            # shared formatting
            ax.set_xlabel(conf.xlabel or x)
            ax.set_ylabel(conf.ylabel or y, rotation=0, labelpad=5, ha="right", va="bottom")
            ax.set_title(conf.title or None)

            self.reduce_ticks(ax, self.df[x].to_numpy(), self.df[y].to_numpy())
            self.keep_x_y_axes(ax)
            ax.grid(False)

        plt.savefig(outpath, format="pdf", bbox_inches="tight")
        plt.close(fig)
