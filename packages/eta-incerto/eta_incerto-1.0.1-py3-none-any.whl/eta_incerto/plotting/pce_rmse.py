from pathlib import Path

import h5py
import matplotlib.pyplot as plt
from pandas import DataFrame

from eta_incerto.config.config_plotting import ConfigPlotting
from eta_incerto.config.config_problem import ConfigProblem


class PceRmsePlotter:
    def __init__(self, problem_config: ConfigProblem, h5_folder_path: str, h5_file: str):
        folder = Path(h5_folder_path)
        self.h5_file = folder / h5_file
        if not self.h5_file.exists():
            raise FileNotFoundError(f"HDF5 file not found: {self.h5_file}")

        self.df, self.orders, self.order_labels = self._load_h5(problem_config)

    def _load_h5(self, config) -> tuple[DataFrame, list[int], list[str]]:
        """Load RMSE results from HDF5 into a DataFrame."""
        with h5py.File(self.h5_file, "r") as f:
            design_x_range = f["rmse/design_var"][:]
            rmse_matrix = f["rmse/matrix"][:]
            orders = f["rmse/orders"][:]
            order_labels = [n.decode() if isinstance(n, bytes) else str(n) for n in f["rmse/order_labels"][:]]

        # Build dataframe
        data = {"design_var": design_x_range}
        for i, lbl in enumerate(order_labels):
            data[lbl] = rmse_matrix[:, i]
        rmse_df = DataFrame(data)

        return rmse_df, orders, order_labels

    @staticmethod
    def keep_x_y_axes(ax):
        """Keep only bottom and left spines, remove top and right."""
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["bottom"].set_visible(True)
        ax.spines["left"].set_visible(True)

    def plot_all_orders(self, config: ConfigPlotting, outpath: str):
        """
        Plot RMSE vs nominal power for all PCE orders in one figure.
        """
        plt.rcParams.update(config.rcparams)

        fig, ax = plt.subplots(figsize=(config.fig_w_in, config.fig_h_in), constrained_layout=True)

        # plot each order curve
        for lbl in self.order_labels:
            ax.plot(
                self.df["design_var"],
                self.df[lbl],
                label=lbl,
                linewidth=2,
            )

        # formatting
        ax.set_xlabel("Design variable")
        ax.set_ylabel("RMSE on design variable set", rotation=0, labelpad=5, ha="right", va="bottom")
        ax.set_title("RMSE vs. design variable for different PCE orders")
        ax.legend(title="PCE order")
        ax.grid(True)
        self.keep_x_y_axes(ax)

        # save to file
        plt.savefig(outpath, format="pdf", bbox_inches="tight")
        plt.close(fig)
