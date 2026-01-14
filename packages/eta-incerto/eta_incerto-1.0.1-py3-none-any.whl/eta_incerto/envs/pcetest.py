from __future__ import annotations

from logging import getLogger
from pathlib import Path

import h5py
from chaospy import fit_regression, generate_expansion
from chaospy.distributions.baseclass import Distribution
from joblib import Parallel, delayed
from numpy import (
    arange,
    array,
    asarray,
    mean as npmean,
    ndarray,
    sqrt,
    zeros,
)
from pydantic import BaseModel, ConfigDict, Field

from eta_incerto.config.config import ConfigOptimization
from eta_incerto.envs.model import Model

log = getLogger(__name__)


class PceOrderTest(BaseModel):
    """Evaluate for a variant model the pce surrogate model qualtiy with RMSE."""

    model_config = ConfigDict(arbitrary_types_allowed=True)
    config: ConfigOptimization = Field(..., description="Optimization config from central config.json")
    distribution_data: Distribution = Field(..., description="Distribution of input parameters")
    model_builder: Model = Field(..., description="Model to use for evaluation")
    h5_file_name: str

    def design_vector(self):
        """Builds a design vector with maximum, minimum dimension with step length."""
        return arange(
            self.config.pcetest.design_var_min, self.config.pcetest.design_var_max, self.config.pcetest.design_var_step
        )

    def rmse_matrix(self):
        """Builds matrix for design."""
        design_x_range = self.design_vector()
        return zeros((len(design_x_range), self.config.pcetest.max_order))

    def model(self, x, xi):
        return self.model_builder.build_simulate_model(x, xi)  # returns LCOE

    def rmse_vs_order(self, design_x):
        n_val = self.config.pcetest.n_val
        max_order = self.config.pcetest.max_order
        sampler = self.config.pcetest.sampler
        n_jobs = self.config.evaluate.n_jobs
        backend = self.config.evaluate.backend

        orders, rmses = [], []

        # validation inputs
        x_val = self.distribution_data.sample(n_val, rule=sampler)

        # true model on validation set
        y_val = Parallel(n_jobs=n_jobs, backend=backend)(
            delayed(self.model)(design_x, x_val[:, i]) for i in range(n_val)
        )
        y_val = array(y_val)

        for order in range(1, max_order + 1):
            pol_basis = generate_expansion(order, self.distribution_data)
            n_train = 2 * len(pol_basis)
            x_train = self.distribution_data.sample(n_train, rule=sampler)

            # keep same parallel config as above for consistency
            y_train = Parallel(n_jobs=n_jobs, backend=backend)(
                delayed(self.model)(design_x, x_train[:, i]) for i in range(n_train)
            )
            y_train = array(y_train)

            pce = fit_regression(pol_basis, x_train, y_train)
            y_pred = asarray(pce(*x_val), dtype=float)

            rmse = sqrt(npmean((y_val - y_pred) ** 2))
            orders.append(order)
            rmses.append(rmse)

        return rmses, orders

    def evaluate_rmse_for_var(self, var):
        design_x = [var]
        rmses, _ = self.rmse_vs_order(design_x)
        return rmses

    def save_rmse_results(self, design_x_range, rmse_matrix) -> None:
        """
        Save RMSE results vs nominal power into a single HDF5 file:
        /rmse/design_var, /rmse/matrix, /rmse/orders, /rmse/order_labels, /config/
        """
        h5_file_name = self.h5_file_name

        out_dir = Path(self.config.paths.results_dir)
        out_dir.mkdir(parents=True, exist_ok=True)

        hdf_path = out_dir / h5_file_name
        if hdf_path.exists():
            hdf_path.unlink()

        with h5py.File(hdf_path, "w") as f:
            f.create_dataset("rmse/design_var", data=design_x_range)
            f.create_dataset("rmse/matrix", data=rmse_matrix)

            orders = arange(1, rmse_matrix.shape[1] + 1)
            f.create_dataset("rmse/orders", data=orders)

            order_labels = array([f"Order {o}" for o in orders], dtype="S")
            f.create_dataset("rmse/order_labels", data=order_labels)

            def save_config(group, d):
                for k, v in d.items():
                    if isinstance(v, dict):
                        subgrp = group.create_group(k)
                        save_config(subgrp, v)
                    elif isinstance(v, (list, tuple, ndarray)):
                        group.create_dataset(k, data=array(v))
                    else:
                        try:
                            group.create_dataset(k, data=v)
                        except TypeError:
                            group.create_dataset(k, data=str(v))

            try:
                config_dict = self.config.to_dict()
            except AttributeError:
                config_dict = self.config.__dict__

            cfg_group = f.create_group("config")
            save_config(cfg_group, config_dict)

        log.info("RMSE results stored: matrix shape %s -> %s", rmse_matrix.shape, hdf_path)

    def evaluate_rmse(self):
        """
        Compute the full RMSE matrix (rows = design points, cols = orders),
        then call save_rmse_results() to persist it.
        """
        rmse_matrix = self.rmse_matrix()
        design_x_range = self.design_vector()

        for i, var in enumerate(design_x_range):
            rmse_matrix[i, :] = self.evaluate_rmse_for_var(var)

        # now save directly
        self.save_rmse_results(design_x_range, rmse_matrix)
