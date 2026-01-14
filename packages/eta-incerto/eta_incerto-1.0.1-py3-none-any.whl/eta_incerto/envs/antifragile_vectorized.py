from __future__ import annotations

import logging

from chaospy import fit_regression, generate_expansion, generate_quadrature
from numpy import (
    array,
    asarray,
    inf,
    median,
    sqrt,
    sum as np_sum,
)
from pymoo.core.problem import ElementwiseProblem
from scipy.stats import skew

from eta_incerto.config.config_antifragile import AntifragileConfig

logger = logging.getLogger(__name__)


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

    def model(self, x, samples):
        return self.cfg.model_builder.build_simulate_model(x, samples)  # returns LCOE

    def build_pce_surrogate(self, x, distribution_data, pce_rule, pce_order):
        poly_exp = generate_expansion(order=pce_order, dist=distribution_data)

        # Samples shape: (n_vars, n_samples). Transpose to (n_samples, n_vars)
        samples = distribution_data.sample(2 * len(poly_exp), rule=pce_rule).T

        # Fully vectorized evaluation
        y_vals = self.model(x, samples)

        return fit_regression(poly_exp, samples.T, y_vals)

    def upr_from_distribution(self, pce_model, distribution_data, omega, quad_order, quad_rule):
        nodes, weights = generate_quadrature(order=quad_order, dist=distribution_data, rule=quad_rule)

        # Evaluate model at quadrature nodes
        y = pce_model(*nodes)  # this gives predicted outcomes, not inputs

        upside = np_sum((y - omega) * weights * (y > omega))
        downside_sq = np_sum(((y - omega) ** 2) * weights * (y < omega))
        downside = sqrt(downside_sq)

        return upside / downside if downside > 0 else inf

    def evaluate_statistics(
        self, pce_model, distribution_data, stat_n_mc, stat_omega, stat_rule, quad_order, quad_rule
    ):
        samples = distribution_data.sample(stat_n_mc, stat_rule)
        y = pce_model(*samples)
        y = asarray(y, dtype=float)
        med = median(y)
        skewness = skew(y)
        upr = self.upr_from_distribution(pce_model, distribution_data, stat_omega, quad_order, quad_rule)
        return array([med, -skewness, -upr])

    def _evaluate(self, x, out, *args, **kwargs):
        pce_model = self.build_pce_surrogate(
            x, self.cfg.distribution_data, self.cfg.config.evaluate.pce_rule, self.cfg.config.evaluate.pce_order
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
            out["F"] = (stats - self.obj_min) / (self.obj_max - self.obj_min + 1e-12)
        else:
            out["F"] = stats  # raw [median, skewness, upr]
