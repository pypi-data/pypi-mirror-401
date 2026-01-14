from __future__ import annotations

from copy import deepcopy
from logging import INFO, basicConfig, getLogger
from pathlib import Path
from types import SimpleNamespace
from typing import TYPE_CHECKING

from eta_incerto.config.config import ConfigOptimization
from eta_incerto.config.config_antifragile import AntifragileConfig
from eta_incerto.envs.antifragile import AntifragileProblem
from eta_incerto.envs.deterministic_evaluation import DeterministicEvaluator
from eta_incerto.envs.doe import Doe
from eta_incerto.envs.pcetest import PceOrderTest
from eta_incerto.envs.regret_evaluation import RegretEvaluator
from eta_incerto.envs.robust_evaluation import RobustEvaluator
from eta_incerto.envs.scenario import Scenario, ScenarioCollection
from eta_incerto.envs.stochastic import StochasticScenario, StochasticScenarioCollection
from eta_incerto.envs.stochastic_evaluation import StochasticEvaluator
from eta_incerto.plotting.doe_plotter import DoePlotter
from eta_incerto.plotting.pareto import ParetoPlotter
from eta_incerto.plotting.pce_rmse import PceRmsePlotter
from eta_incerto.plotting.performance import PerformancePlot
from eta_incerto.plotting.report import A4SummaryReport
from eta_incerto.plotting.topology import TopologyPlot
from eta_incerto.registry import get_system

if TYPE_CHECKING:
    import os

basicConfig(level=INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", force=True)

log = getLogger(__name__)


class EtaIncerto:
    """Orchestrator for the optimization."""

    def __init__(
        self,
        root_path: str | os.PathLike,
        config_name: str,
        relpath_config: str | os.PathLike = "config/",
    ) -> None:
        _root_path = root_path if isinstance(root_path, Path) else Path(root_path)
        __relpath_config_file = relpath_config if isinstance(relpath_config, Path) else Path(relpath_config)
        self.path_config_file = _root_path / __relpath_config_file / f"{config_name}"
        self.config: ConfigOptimization = ConfigOptimization.from_file(self.path_config_file, _root_path)
        self.scenarios = ScenarioCollection()
        self.invest_scenarios = ScenarioCollection()
        self.stochastic_scenarios = StochasticScenarioCollection()
        self.invest_stochastic_scenarios = StochasticScenarioCollection()

    # loading of data and configuration
    def load_system_series_scenario(self):
        """Load all systems, series, energy scenarios and store it in scenarios"""
        for system_name in self.config.system.name:
            system_cls, static_data_cls, investment_data_cls, _ = get_system(system_name)
            static_data = static_data_cls.load_default()
            investment_data = investment_data_cls.load_default()
            system_builder = system_cls(self.config, static_data, investment_data)

            base_static_system = system_builder.build_static_system()

            for series in self.config.series.series_file:
                for scenario in self.config.scenario.scenario_file:
                    dims = SimpleNamespace(
                        n_years=self.config.system.n_years,
                        n_periods=self.config.system.n_periods,
                        n_time_steps=self.config.system.n_time_steps,
                        year_length=self.config.system.year_length,
                        step_length=series.step_length,
                    )
                    carrier_types = self.config.scenario.carrier_types

                    series_data = self.config.series.load_typical_day(self.config, dims, series.file_name)
                    scenario_data = scenario.load_supplier_data(dims, carrier_types)

                    system_copy = deepcopy(base_static_system)
                    scenario_id = f"{system_name}_{series.file_name}_{scenario.name}"

                    dynamic_system = system_builder.build_dynamic_system(system_copy, series_data, scenario_data)

                    baseline_system = deepcopy(dynamic_system)
                    scenario_id_invest = f"{system_name}_{series.file_name}_{scenario.name}_invest"
                    investment_system = system_builder.build_investment(baseline_system)

                    system_series_scenario = Scenario(
                        name=scenario_id,
                        system=dynamic_system,
                        series=series_data,
                        energy_scenario=scenario_data,
                        series_file_name=series.file_name,
                    )
                    self.scenarios.set_scenario(system_series_scenario)

                    invest_scenario = Scenario(
                        name=scenario_id_invest,
                        system=investment_system,
                        series=series_data,
                        energy_scenario=scenario_data,
                        series_file_name=series.file_name,
                    )
                    self.invest_scenarios.set_scenario(invest_scenario)

                    system_series_stochastic_scenario = StochasticScenario(
                        name=scenario_id,
                        system=dynamic_system,
                        series=series_data,
                        energy_scenario=scenario_data,
                        series_file_name=series.file_name,
                        probability=scenario.probability,
                    )
                    self.stochastic_scenarios.set_scenario(system_series_stochastic_scenario)

                    invest_stochastic_scenario = StochasticScenario(
                        name=scenario_id_invest,
                        system=investment_system,
                        series=series_data,
                        energy_scenario=scenario_data,
                        series_file_name=series.file_name,
                        probability=scenario.probability,
                    )
                    self.invest_stochastic_scenarios.set_scenario(invest_stochastic_scenario)

        log.info("Loaded scenarios: %s", list(self.scenarios.names()))
        return self.scenarios, self.stochastic_scenarios, self.invest_scenarios, self.invest_stochastic_scenarios

    def load_stochastic_system_series_scenario(self, variant):
        """Load all systems, series, energy scenarios and store it in scenarios"""
        stochastic_scenarios = StochasticScenarioCollection()
        invest_stochastic_scenarios = StochasticScenarioCollection()

        system_cls, static_data_cls, investment_data_cls, _ = get_system(variant)
        static_data = static_data_cls.load_default()
        investment_data = investment_data_cls.load_default()
        system_builder = system_cls(self.config, static_data, investment_data)

        base_static_system = system_builder.build_static_system()

        for series in self.config.series.series_file:
            for scenario in self.config.scenario.scenario_file:
                dims = SimpleNamespace(
                    n_years=self.config.system.n_years,
                    n_periods=self.config.system.n_periods,
                    n_time_steps=self.config.system.n_time_steps,
                    year_length=self.config.system.year_length,
                    step_length=series.step_length,
                )
                carrier_types = self.config.scenario.carrier_types

                series_data = self.config.series.load_typical_day(self.config, dims, series.file_name)
                scenario_data = scenario.load_supplier_data(dims, carrier_types)

                system_copy = deepcopy(base_static_system)
                scenario_id = f"{variant}_{series.file_name}_{scenario.name}"

                dynamic_system = system_builder.build_dynamic_system(system_copy, series_data, scenario_data)

                baseline_system = deepcopy(dynamic_system)
                scenario_id_invest = f"{variant}_{series.file_name}_{scenario.name}_invest"
                investment_system = system_builder.build_investment(baseline_system)

                system_series_stochastic_scenario = StochasticScenario(
                    name=scenario_id,
                    system=dynamic_system,
                    series=series_data,
                    energy_scenario=scenario_data,
                    series_file_name=series.file_name,
                    probability=scenario.probability,
                )
                stochastic_scenarios.set_scenario(system_series_stochastic_scenario)

                invest_stochastic_scenario = StochasticScenario(
                    name=scenario_id_invest,
                    system=investment_system,
                    series=series_data,
                    energy_scenario=scenario_data,
                    series_file_name=series.file_name,
                    probability=scenario.probability,
                )
                invest_stochastic_scenarios.set_scenario(invest_stochastic_scenario)

        log.info("Loaded scenarios: %s", list(self.scenarios.names()))
        return stochastic_scenarios, invest_stochastic_scenarios

    def load_model_series_algorithm_termination(self):
        """Loads the relevant component (different heat pump models) and the related distributions for the
        input parameters."""
        for variant in self.config.system.name:  # TODO @m.frank: #3 make it work with list of names
            system_cls, static_data_cls, investment_data_cls, distribution_data_cls = get_system(variant)
            static_data = static_data_cls.load_default()
            distribution_data = distribution_data_cls.load_default().build_joint()
            investment_data = investment_data_cls.load_default()
            model_builder = system_cls(config=self.config, investment_data=investment_data, static_data=static_data)
            for series in self.config.series.series_file:
                demand_series = self.config.series.load_series_df(self.config, series.file_name)
        log.info("Loaded model builder: %s", variant)
        return model_builder, demand_series, distribution_data

    # deterministic invest optimization

    def evaluate_deterministic(self, scenarios: ScenarioCollection | None = None):
        """Evaluate baseline scenarios."""
        if scenarios is None:
            scenarios = self.scenarios
        evaluator = DeterministicEvaluator(config=self.config, scenarios=scenarios, h5_file_name="determ_wo_invest.h5")
        return evaluator.evaluate_systems()

    def evaluate_operation_with_invest(self, invest_scenarios: ScenarioCollection | None = None):
        """Attach to each built scenario the investment and evaluate."""
        if invest_scenarios is None:
            invest_scenarios = self.invest_scenarios
        evaluator = DeterministicEvaluator(
            config=self.config, scenarios=invest_scenarios, h5_file_name="determ_w_invest.h5"
        )
        return evaluator.evaluate_systems()

    # conventional invest under uncertainty optimization
    def stochastic_optimization(self):
        """Attach to each built scenario the investment and stochastically evaluate."""
        for variant in self.config.system.variant:
            h5_file_name = f"stochastic_{variant}.h5"
            _, stochastic_invest_scenarios = self.load_stochastic_system_series_scenario(variant)
            evaluator = StochasticEvaluator(
                config=self.config, scenarios=stochastic_invest_scenarios, h5_file_name=h5_file_name
            )
            evaluator.evaluate_systems()

    def robust_optimization(self):
        """Evaluate robust scenarios."""
        for variant in self.config.system.variant:
            h5_file_name = f"robust_{variant}.h5"
            _, stochastic_invest_scenarios = self.load_stochastic_system_series_scenario(variant)
            evaluator = RobustEvaluator(
                config=self.config, scenarios=stochastic_invest_scenarios, h5_file_name=h5_file_name
            )
            evaluator.evaluate_systems()

    def regret_optimization(self):
        """Evaluate regret scenarios."""
        for variant in self.config.system.variant:
            h5_file_name = f"regret_{variant}.h5"
            _, stochastic_invest_scenarios = self.load_stochastic_system_series_scenario(variant)
            evaluator = RegretEvaluator(
                config=self.config, scenarios=stochastic_invest_scenarios, h5_file_name=h5_file_name
            )
            evaluator.evaluate_systems()

    def summary_plot(self):
        path_w0_invest = self.config.paths.results_dir / "stochastic_expected.h5"
        path_w_invest = self.config.paths.results_dir / "stochastic_expected_with_invest_opex.h5"
        perf = PerformancePlot(path_w0_invest, path_w_invest)
        topo_wo_invest = TopologyPlot(h5_path=path_w0_invest)
        topo_w_invest = TopologyPlot(h5_path=path_w_invest)

        report = A4SummaryReport(
            perf=perf,
            topo_wo=topo_wo_invest,
            topo_w=topo_w_invest,
            path_wo_invest=path_w0_invest,
            path_w_invest=path_w_invest,
            title="Heat Pump Optimization - Summary",
            subtitle="Expected performance + topology",
            footer_right="Michael Frank",
        )
        out_pdf = self.config.paths.plots_dir / "investment_summary_sheet.pdf"
        report.save(out_pdf)
        return out_pdf

    def evaluate_antifragile_doe(self, model_builder, demand_series, distribution_data):
        """Conduct a Design of Experiments and plot results."""
        doe_run = Doe(
            config=self.config,
            model_builder=model_builder,
            demand_series=demand_series,
            distribution_data=distribution_data,
            h5_file_name=self.config.doe.h5_filename,
            variable_names=self.config.problem.variable_names,
            objective_names=self.config.problem.objective_names,
        )
        doe_run.conduct_doe()

        plotter = DoePlotter(self.config.plotting, self.config.paths.results_dir, "doe_experiment.h5")
        plotter.plot(self.config.plotting, Path(self.config.paths.plots_dir) / "doe_experiment.pdf")
        plotter.plot_sobol_indices(self.config.plotting, Path(self.config.paths.plots_dir) / "sobol_indices.pdf")
        log.info("PCE test plotted to doe_experiment.pdf")

    def evaluate_pce_order(self, model_builder, distribution_data):
        """Evaluate for a variant model the pce surrogate model qualtiy with RMSE."""
        surrogate_model_test = PceOrderTest(
            config=self.config,
            model_builder=model_builder,
            distribution_data=distribution_data,
            h5_file_name="pce_order_test.h5",
        )
        surrogate_model_test.evaluate_rmse()
        plotter = PceRmsePlotter(self.config.plotting, self.config.paths.results_dir, "pce_order_test.h5")
        plotter.plot_all_orders(self.config.plotting, Path(self.config.paths.plots_dir) / "pce_order_test.pdf")
        log.info("PCE test plotted to pce_order_test.pdf")

    def run_analysis(self) -> None:
        """Run optional analysis modules based on the configuration."""
        if not self.config.analysis.enabled:
            return

        if self.config.analysis.mode == "std_target":
            from eta_incerto.analysis.sensitivity import (
                run_std_target_sensitivity_from_config,
            )

            run_std_target_sensitivity_from_config(self.config)
            return

        raise ValueError(f"Unsupported analysis mode: {self.config.analysis.mode}")

    def evaluate_antifragile(self, model_builder, demand_series, distribution_data):
        """Evaluate for a component the antifragile dimension compared to lcoe."""
        cfg = AntifragileConfig(
            config=self.config,
            model_builder=model_builder,
            demand_series=demand_series,
            distribution_data=distribution_data,
            h5_file_name="antifragile.h5",
            variable_names=self.config.problem.variable_names,
            objective_names=self.config.problem.objective_names,
        )
        problem = AntifragileProblem(cfg)
        problem.evaluate_system()
        plotter = ParetoPlotter(cfg.config.problem, cfg.config.paths.results_dir, cfg.h5_file_name)
        plotter.plot(cfg.config.plotting, Path(cfg.config.paths.plots_dir) / f"{cfg.h5_file_name}.pdf")
