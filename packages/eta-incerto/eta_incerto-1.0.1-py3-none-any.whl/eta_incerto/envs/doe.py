from __future__ import annotations

from logging import getLogger
from pathlib import Path

import h5py
from chaospy.distributions.baseclass import Distribution
from numpy import array, ndarray
from pandas import DataFrame
from pydantic import BaseModel, ConfigDict
from pymoo.operators.sampling.lhs import LHS
from pymoo.operators.sampling.rnd import FloatRandomSampling
from SALib.analyze import sobol
from SALib.sample import saltelli

from eta_incerto.config.config import ConfigOptimization
from eta_incerto.config.config_antifragile import AntifragileConfig
from eta_incerto.envs.antifragile import AntifragileProblem
from eta_incerto.envs.model import Model

DOE_METHODS = {"lhs": LHS(), "random": FloatRandomSampling()}

log = getLogger(__name__)


class Doe(BaseModel):
    """Evaluate surrogate model quality with DOE sampling."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    config: ConfigOptimization
    distribution_data: Distribution
    model_builder: Model
    demand_series: DataFrame
    h5_file_name: str
    variable_names: str | list[str]
    objective_names: str | list[str]

    def _sample_inputs(self, problem, n_samples: int) -> ndarray:
        sampler = DOE_METHODS.get(self.config.doe.method)
        if sampler is None:
            raise ValueError(f"Unknown DOE method: {self.config.doe.method}")
        return sampler(problem, n_samples).get("X")

    def conduct_doe(self):
        """Sample and conduct the actual DOE."""
        cfg = AntifragileConfig(
            config=self.config,
            model_builder=self.model_builder,
            demand_series=self.demand_series,
            distribution_data=self.distribution_data,
            h5_file_name=self.h5_file_name,
            variable_names=self.variable_names,
            objective_names=self.objective_names,
        )
        problem = AntifragileProblem(cfg)

        n_samples = self.config.doe.n_samples

        x_samples = self._sample_inputs(problem, n_samples)

        f_results = []
        for x_i in x_samples:
            out = {}
            problem._evaluate(x_i, out=out)
            f_results.append(out["F"])

        f_results = array(f_results)
        f_min, f_max = f_results.min(axis=0), f_results.max(axis=0)
        log.info("DOE ranges: %s .. %s", f_min, f_max)

        # conduct sobol indices analysis

        def get_bounds_from_distribution(distribution_data, quantiles=(0.01, 0.99)):
            bounds = []
            for dist in distribution_data:
                lo, hi = dist.ppf(quantiles)  # quantile-based bounds
                # replace infinities with wide finite values if needed
                if lo == -float("inf"):
                    lo = float(dist.ppf(0.001))
                if hi == float("inf"):
                    hi = float(dist.ppf(0.999))
                bounds.append([float(lo), float(hi)])
            return bounds

        bounds = get_bounds_from_distribution(cfg.distribution_data)

        sobol_results = self.conduct_sobol(bounds)

        self._save_results(cfg, x_samples, f_results, self.h5_file_name, sobol_results)

        return x_samples, f_results, f_min, f_max

    def conduct_sobol(self, bounds: list[tuple[float, float]]):
        """Perform Sobol sensitivity analysis."""
        # Normalize variable names
        dist_names = self.config.doe.dist_names

        problem = {
            "num_vars": len(dist_names),
            "names": dist_names,
            "bounds": bounds,
        }

        # Generate Sobol samples
        n_samples = self.config.doe.n_samples
        param_values = saltelli.sample(problem, N=n_samples, calc_second_order=True)

        # Evaluate
        cfg = AntifragileConfig(
            config=self.config,
            model_builder=self.model_builder,
            demand_series=self.demand_series,
            distribution_data=self.distribution_data,
            h5_file_name=self.h5_file_name,
            variable_names=self.variable_names,
            objective_names=self.objective_names,
        )
        problem_eval = AntifragileProblem(cfg)

        y = []
        for x in param_values:
            out = {}
            problem_eval._evaluate(x, out=out)
            y.append(out["F"])  # multi-objective possible

        y = array(y)

        # Compute Sobol indices for each objective
        sobol_results = {}
        for i, obj_name in enumerate(
            self.objective_names if isinstance(self.objective_names, list) else [self.objective_names]
        ):
            si = sobol.analyze(problem, y[:, i], print_to_console=False)
            sobol_results[obj_name] = si

        return sobol_results

    def _save_results(
        self, cfg, x: ndarray, fvals: ndarray, h5_file_name: str, sobol_results: dict | None = None
    ) -> None:
        """Save DOE results (and optionally Sobol indices) to HDF5."""
        out_dir = Path(self.config.paths.results_dir)
        out_dir.mkdir(parents=True, exist_ok=True)

        hdf_path = out_dir / h5_file_name
        if hdf_path.exists():
            hdf_path.unlink()

        with h5py.File(hdf_path, "w") as f:
            f.create_dataset("doe/X", data=x)
            f.create_dataset("doe/F", data=fvals)

            # Normalize variable/objective names
            var_names = cfg.variable_names if isinstance(cfg.variable_names, list) else [cfg.variable_names]
            obj_names = cfg.objective_names if isinstance(cfg.objective_names, list) else [cfg.objective_names]

            if len(var_names) != x.shape[1]:
                raise ValueError(f"Expected {x.shape[1]} variable names, got {len(var_names)}")
            if len(obj_names) != fvals.shape[1]:
                raise ValueError(f"Expected {fvals.shape[1]} objective names, got {len(obj_names)}")

            f.create_dataset("doe/variable_names", data=array(var_names, dtype="S"))
            f.create_dataset("doe/objective_names", data=array(obj_names, dtype="S"))

            # save Sobol results if provided
            if sobol_results is not None:
                sobol_group = f.create_group("doe/sobol")
                for obj, res in sobol_results.items():
                    obj_group = sobol_group.create_group(obj)
                    for k, v in res.items():
                        try:
                            obj_group.create_dataset(k, data=array(v))
                        except Exception:
                            obj_group.create_dataset(k, data=str(v))

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

            config_dict = getattr(cfg.config, "to_dict", lambda: cfg.config.__dict__)()
            save_config(f.create_group("config"), config_dict)

        log.info(
            "DOE stored: x %s, f %s with %d vars, %d objs%s -> %s",
            x.shape,
            fvals.shape,
            len(var_names),
            len(obj_names),
            " and Sobol indices" if sobol_results is not None else "",
            hdf_path,
        )
