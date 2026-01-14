from __future__ import annotations

from logging import getLogger
from pathlib import Path

import h5py
from chaospy import fit_regression, generate_expansion, generate_quadrature
from joblib import Parallel, delayed
from numpy import (
    array,
    asarray,
    inf,
    median,
    ndarray,
    sqrt,
    sum as np_sum,
)
from pymoo.core.problem import ElementwiseProblem
from pymoo.optimize import minimize
from scipy.stats import skew

from eta_incerto.config.config_antifragile import AntifragileConfig

log = getLogger(__name__)


class AntifragileProblem(ElementwiseProblem):
    """Evaluate components antifragile."""

    def __init__(self, cfg: AntifragileConfig, **kwargs):
        self.cfg = cfg
        n_var = cfg.config.problem.n_variables
        n_obj = cfg.config.problem.n_objectives
        n_constr = cfg.config.problem.n_eq_constraints
        xl = cfg.config.problem.x_lower_bound
        xu = cfg.config.problem.x_upper_bound
        self.normalize = cfg.config.problem.normalize
        self.obj_min = array(cfg.config.problem.obj_min, dtype=float)
        self.obj_max = array(cfg.config.problem.obj_max, dtype=float)
        super().__init__(n_var=n_var, n_obj=n_obj, n_constr=n_constr, xl=xl, xu=xu, elementwise=True, **kwargs)

    def model(self, x, xi):
        return self.cfg.model_builder.build_simulate_model(x, xi)  # returns LCOE

    def build_pce_surrogate(self, x, distribution_data, pce_rule, pce_order, n_jobs, backend):
        poly_exp = generate_expansion(order=pce_order, dist=distribution_data)

        # Samples shape: (n_vars, n_samples). Transpose to (n_samples, n_vars)
        samples = distribution_data.sample(4 * len(poly_exp), rule=pce_rule)
        y_vals = Parallel(n_jobs=n_jobs, backend=backend)(
            delayed(self.model)(x, samples[:, i]) for i in range(samples.shape[1])
        )
        return fit_regression(poly_exp, samples, y_vals)

    def upr_from_distribution(self, pce_model, distribution_data, omega, quad_order, quad_rule):
        """Adapted for accepting costs."""
        nodes, weights = generate_quadrature(order=quad_order, dist=distribution_data, rule=quad_rule)

        # Evaluate model at quadrature nodes
        y = pce_model(*nodes)  # predicted outcomes

        # Upside: expected positive deviations above omega
        upside = np_sum((omega - y) * weights * (y < omega))

        # Downside: root mean squared negative deviations below omega
        downside = sqrt(np_sum(((omega - y) ** 2) * weights * (y > omega)))

        return upside / downside if downside > 0 else inf

    def evaluate_statistics(
        self, pce_model, distribution_data, stat_n_mc, stat_omega, stat_rule, quad_order, quad_rule
    ):
        samples = distribution_data.sample(stat_n_mc, stat_rule)
        y = asarray(pce_model(*samples), dtype=float)

        # statistical metrics
        med = median(y)
        skewness = skew(y)
        upr = self.upr_from_distribution(pce_model, distribution_data, stat_omega, quad_order, quad_rule)

        return array([med, -skewness, upr])

    def _evaluate(self, x, out, *args, **kwargs):
        pce_model = self.build_pce_surrogate(
            x,
            self.cfg.distribution_data,
            self.cfg.config.evaluate.pce_rule,
            self.cfg.config.evaluate.pce_order,
            self.cfg.config.evaluate.n_jobs,
            self.cfg.config.evaluate.backend,
        )
        stats = self.evaluate_statistics(
            pce_model,
            self.cfg.distribution_data,
            self.cfg.config.evaluate.stat_n_mc,
            self.cfg.config.evaluate.stat_omega,
            self.cfg.config.evaluate.stat_rule,
            self.cfg.config.evaluate.quad_order,
            self.cfg.config.evaluate.quad_rule,
        )
        if self.normalize:
            out["F"] = (stats - self.obj_min) / (self.obj_max - self.obj_min)
        else:
            out["F"] = stats  # raw [median, skewness, upr]

    def evaluate_system(self):
        algorithm_cfg = self.cfg.config.algorithm
        termination = self.cfg.config.termination.termination_instance
        algorithm = algorithm_cfg.algorithm_class(
            pop_size=algorithm_cfg.pop_size,
            sampling=algorithm_cfg.sampling_class(),
            selection=algorithm_cfg.selection_class(),
            crossover=algorithm_cfg.crossover_class(),
            mutation=algorithm_cfg.mutation_class(),
        )

        res = minimize(
            self, algorithm, termination, seed=self.cfg.config.settings.seed, verbose=self.cfg.config.settings.verbose
        )
        self._save_results(res.X, res.F, self.cfg.h5_file_name)

    def _save_results(self, x: ndarray, fvals: ndarray, h5_file_name: str) -> None:
        """Save optimization results to HDF5 (no 'doe' group)."""
        out_dir = Path(self.cfg.config.paths.results_dir)
        out_dir.mkdir(parents=True, exist_ok=True)

        hdf_path = out_dir / h5_file_name
        if hdf_path.exists():
            hdf_path.unlink()

        with h5py.File(hdf_path, "w") as f:
            # store X and F directly at the root level
            f.create_dataset("pareto/X", data=x)
            f.create_dataset("pareto/F", data=fvals)

            # Normalize variable/objective names
            var_names = self.cfg.variable_names
            if isinstance(var_names, str):
                var_names = [var_names]
            if len(var_names) != x.shape[1]:
                raise ValueError(f"Expected {x.shape[1]} variable names, got {len(var_names)}")

            obj_names = self.cfg.objective_names
            if isinstance(obj_names, str):
                obj_names = [obj_names]
            if len(obj_names) != fvals.shape[1]:
                raise ValueError(f"Expected {fvals.shape[1]} objective names, got {len(obj_names)}")

            # store metadata at the root as well
            f.create_dataset("pareto/variable_names", data=array(var_names, dtype="S"))
            f.create_dataset("pareto/objective_names", data=array(obj_names, dtype="S"))

            # recursive config saving
            def save_config(group, d):
                for k, v in d.items():
                    if isinstance(v, dict):
                        save_config(group.create_group(k), v)
                    elif isinstance(v, (list, tuple, ndarray)):
                        group.create_dataset(k, data=array(v))
                    else:
                        try:
                            group.create_dataset(k, data=v)
                        except TypeError:
                            group.create_dataset(k, data=str(v))

            config_dict = getattr(self.cfg.config, "to_dict", lambda: self.cfg.config.__dict__)()
            save_config(f.create_group("config"), config_dict)

        log.info(
            "Optimization results stored: x %s, f %s with %d vars, %d objs -> %s",
            x.shape,
            fvals.shape,
            len(var_names),
            len(obj_names),
            hdf_path,
        )
