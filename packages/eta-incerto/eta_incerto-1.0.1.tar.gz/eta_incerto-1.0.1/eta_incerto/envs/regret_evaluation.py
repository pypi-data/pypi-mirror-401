# eta_incerto/evaluation/regret_evaluation.py
from __future__ import annotations

import datetime as dt
import logging
from collections import defaultdict
from collections.abc import Iterator
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

import h5py
from eta_components.milp_component_library.custom_types import BasicSystem
from eta_components.milp_component_library.objectives import Emissions, NetPresentValue
from numpy import (
    allclose as np_allclose,
    array,
    asarray,
    isnan,
    ndarray,
    zeros,
)
from pydantic import BaseModel, ConfigDict, Field
from pyomo.environ import value

from eta_incerto.config.config import ConfigOptimization
from eta_incerto.envs.base import ScenarioCollection
from eta_incerto.envs.robust import RobustFramework
from eta_incerto.envs.stochastic import StochasticScenarioCollection
from eta_incerto.envs.utils import aggregate_over_all_indices

logger = logging.getLogger(__name__)


@dataclass
class _ExpectedAccumulators:
    prob_sum: float = 0.0
    total_emissions_t: float = 0.0
    capex: float = 0.0

    energy_mwh: dict[str, float] = field(default_factory=dict)
    costs_keur: dict[str, float] = field(default_factory=dict)
    emissions_t_by_trader: dict[str, float] = field(default_factory=dict)

    invest_bought: dict[str, float] = field(default_factory=dict)
    invest_p_out_nom: dict[str, float] = field(default_factory=dict)
    invest_cost: dict[str, float] = field(default_factory=dict)

    def add_weighted(self, dct: dict[str, float], key: str, prob: float, val: float) -> None:
        dct[key] = dct.get(key, 0.0) + prob * val


class RegretEvaluator(BaseModel):
    """Solve a regret program and persist objectives + KPIs to HDF5."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    config: ConfigOptimization = Field(..., description="Optimization config from central config.json")
    scenarios: ScenarioCollection = Field(..., description="Scenarios with probabilities")
    h5_file_name: str

    # -----------------------
    # eta-components helpers
    # -----------------------

    def _iter_traders(self, system: BasicSystem) -> Iterator[tuple[str, Any]]:
        """Yield (name, unit) for all units that look like traders."""
        for unit in system.units:
            if all(hasattr(unit, attr) for attr in ("amount", "time_step_cost", "emissions")):
                yield unit.name, unit

    def _iter_investments(self, system: BasicSystem) -> Iterator[tuple[str, Any]]:
        """Yield (name, unit) for all units that look like dimensioning investments."""
        for unit in system.units:
            if all(hasattr(unit, attr) for attr in ("is_bought", "_p_out_nom", "onetime_cost")):
                yield unit.name, unit
                continue
            if hasattr(unit, "model") and all(hasattr(unit.model, a) for a in ("y", "p_out_nom", "investment_cost")):
                yield unit.name, unit

    def _total_investment_cost(self, system: BasicSystem) -> float:
        """Total CAPEX = sum of onetime_cost over all dimensioning investments."""
        total = 0.0
        for _, inv_unit in self._iter_investments(system):
            try:
                total += float(value(inv_unit.onetime_cost))
            except Exception:
                total += float(value(inv_unit.model.investment_cost))
        return total

    # -----------------------
    # HDF5 helpers
    # -----------------------

    def _as_h5_str_array(self, values: list[str]) -> ndarray:
        dt_s = h5py.string_dtype(encoding="utf-8")
        return array(values, dtype=dt_s)

    def _write_topology(self, f: h5py.File, graph: dict[str, Any]) -> None:
        """graph = {'nodes': [str, ...], 'edges': [(str, str), ...]}"""
        topo = f.require_group("topology")

        for key in ("nodes", "edges"):
            if key in topo:
                del topo[key]

        nodes = list(graph.get("nodes", []))
        edges = list(graph.get("edges", []))

        topo.create_dataset("nodes", data=self._as_h5_str_array(nodes))

        if len(edges) == 0:
            topo.create_dataset("edges", data=array([], dtype=h5py.string_dtype("utf-8")).reshape(0, 2))
            return

        def _edge_uv(e):
            if isinstance(e, dict):
                return e["source"], e["target"]
            return e[0], e[1]

        flat = [_edge_uv(e) for e in edges]
        dt_s = h5py.string_dtype(encoding="utf-8")
        topo.create_dataset("edges", data=array(flat, dtype=dt_s))

    def _write_meta_time_tag(self, f: h5py.File, tz_name: str = "Europe/Berlin") -> str:
        tz = ZoneInfo(tz_name)
        now = dt.datetime.now(tz=tz)

        time_tag = now.strftime("%Y%m%d_%H%M%S_%z")
        generated_at = now.isoformat(timespec="seconds")

        meta = f.require_group("meta")
        for key in ("time_tag", "generated_at", "timezone"):
            if key in meta:
                del meta[key]

        meta.create_dataset("time_tag", data=time_tag)
        meta.create_dataset("generated_at", data=generated_at)
        meta.create_dataset("timezone", data=tz_name)
        return time_tag

    # -----------------------
    # Input scenario storage (YEARLY, DISCRETE)
    # -----------------------

    def _collapse_to_year_discrete(
        self,
        d: dict[tuple[int, int, int], float],
        *,
        mode: str = "assert_constant",  # "assert_constant" | "first"
        rtol: float = 0.0,
        atol: float = 0.0,
    ) -> dict[int, float]:
        """
        Collapse {(year, period, timestep): value} -> {year: value} WITHOUT averaging.

        mode="first":          take first encountered value per year
        mode="assert_constant": assert all values within a year are equal (within tol)
        """
        buckets: dict[int, list[float]] = defaultdict(list)
        for (y, _p, _t), v in d.items():
            buckets[int(y)].append(float(v))

        out: dict[int, float] = {}
        for y, vals in buckets.items():
            if not vals:
                continue

            if mode == "first":
                out[y] = vals[0]
                continue

            if mode == "assert_constant":
                v0 = vals[0]
                if not np_allclose(vals, v0, rtol=rtol, atol=atol):
                    raise ValueError(
                        f"Scenario input not discrete for year={y}: "
                        f"min={min(vals):.6g}, max={max(vals):.6g}, expected constant."
                    )
                out[y] = v0
                continue

            raise ValueError(f"Unknown mode={mode}")

        return out

    def _write_year_map(self, grp: h5py.Group, name: str, year_map: dict[int, float]) -> None:
        """
        Store {year: value} as:
          /<name>/year  (N,) int
          /<name>/value (N,) float
        """
        sub = grp.require_group(name)
        for k in ("year", "value"):
            if k in sub:
                del sub[k]

        if not year_map:
            sub.create_dataset("year", data=zeros((0,), dtype=int))
            sub.create_dataset("value", data=zeros((0,), dtype=float))
            return

        years = asarray(sorted(year_map.keys()), dtype=int)
        vals = asarray([year_map[int(y)] for y in years], dtype=float)

        sub.create_dataset("year", data=years)
        sub.create_dataset("value", data=vals)

    def _write_input_scenarios_yearly(self, f: h5py.File, scenarios: ScenarioCollection) -> None:
        """
        Writes yearly *input* scenario data (no period/timestep dims).

        Layout:
          /scenarios/<scenario_name>/probability
          /scenarios/<scenario_name>/carriers/<carrier>/unit_price/{year,value}
          /scenarios/<scenario_name>/carriers/<carrier>/emissions_per_unit/{year,value}
          /scenarios/<scenario_name>/carriers/<carrier>/aggregation
        """
        root = f.require_group("scenarios")
        # overwrite whole section
        for k in list(root.keys()):
            del root[k]

        for scen in scenarios:
            sg = root.create_group(scen.name)
            sg.create_dataset("probability", data=float(getattr(scen, "probability", 0.0)))

            carriers_grp = sg.require_group("carriers")
            energy = getattr(scen, "energy_scenario", None)
            if energy is None:
                continue

            items = energy.items() if isinstance(energy, dict) else [("default", energy)]

            for carrier, supplier in items:
                cg = carriers_grp.require_group(str(carrier))

                unit_price = getattr(supplier, "unit_price", None)
                emissions = getattr(supplier, "emissions_per_unit", None)

                up_year = self._collapse_to_year_discrete(dict(unit_price or {}), mode="assert_constant")
                em_year = self._collapse_to_year_discrete(dict(emissions or {}), mode="assert_constant")

                self._write_year_map(cg, "unit_price", up_year)
                self._write_year_map(cg, "emissions_per_unit", em_year)

                if "aggregation" in cg:
                    del cg["aggregation"]
                cg.create_dataset("aggregation", data="discrete_assert_constant")

    # -----------------------
    # Save results
    # -----------------------

    def _save_results(
        self,
        results: dict[str, dict[Any, Any]],
        h5_file_name: str,
        system: RobustFramework,
        scenarios: ScenarioCollection,
    ) -> None:
        """Save evaluation results + topology + input scenario data to a single HDF5 file."""
        out_dir = Path(self.config.paths.results_dir)
        out_dir.mkdir(parents=True, exist_ok=True)

        hdf_path = out_dir / h5_file_name
        if hdf_path.exists():
            hdf_path.unlink()

        graph = system.graph_representation()

        with h5py.File(hdf_path, "w") as f:
            # meta + topology
            self._write_meta_time_tag(f, tz_name=getattr(self.config, "timezone", "Europe/Berlin"))
            self._write_topology(f, graph)

            # input scenario data (YEARLY)
            self._write_input_scenarios_yearly(f, scenarios)

            # metrics (per scenario)
            for scenario, metrics in results.items():
                grp = f.create_group(scenario)
                for (category, name), value in metrics.items():
                    cat_grp = grp.require_group(category)
                    if name in cat_grp:
                        del cat_grp[name]
                    cat_grp.create_dataset(name, data=value)

            # config
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

            config_dict = getattr(self.config, "to_dict", lambda: self.config.__dict__)()
            save_config(f.create_group("config"), config_dict)

        logger.info("Evaluation results for %d scenarios written to: %s", len(results), hdf_path)

    # -----------------------
    # Objective attachment + solve
    # -----------------------

    def _load_weights(self, series_file_name: str, system: BasicSystem) -> dict[int, float]:
        from json import load

        weights_path = self.config.paths.series_dir / series_file_name / "weights.json"
        if not weights_path.exists():
            raise FileNotFoundError(f"No weights.json found for series {series_file_name}")

        with weights_path.open() as f:
            raw = load(f)
        raw = {int(k): float(v) for k, v in raw.items()}

        weights = {}
        for y in system.years_set:
            for p, w in raw.items():
                weights[(y, p)] = w
        return weights

    def _attach_objectives(self, scenarios: ScenarioCollection) -> None:
        objective_kind = self.config.system.objective
        for scen in scenarios:
            system: BasicSystem = scen.system
            weights = self._load_weights(scen.series_file_name, system)

            npv_obj = NetPresentValue(
                "npv_objective",
                {
                    "weights": weights,
                    "interest": self.config.system.interest,
                    "emission_cost": self.config.system.emission_cost,
                },
                system,
            )
            emissions_obj = Emissions("emissions_objective", {"weights": weights}, system)

            if objective_kind == "npv":
                system.set_objective(npv_obj)
            elif objective_kind == "emissions":
                system.set_objective(emissions_obj)
            else:
                raise ValueError(f"Unknown objective_kind: {objective_kind}")

    def _build_and_solve_framework(self, scenarios: StochasticScenarioCollection) -> RobustFramework:
        fw = RobustFramework(scenarios=scenarios)
        fw.build_model()
        fw.solve(
            solver_name=self.config.settings.solver,
            tee=self.config.settings.tee,
            options=self.config.settings.options,
            model_export=self.config.settings.model_export,
        )
        return fw

    # -----------------------
    # Results collection
    # -----------------------

    def _make_safe_aggregator(self, system: BasicSystem):
        def _safe_agg(var, system=system) -> float:
            return float(aggregate_over_all_indices(var, system))

        return _safe_agg

    def _collect_trader_vals(self, system: BasicSystem, agg) -> dict[str, dict[str, float]]:
        trader_vals: dict[str, dict[str, float]] = {}
        for trader_name, trader in self._iter_traders(system):
            trader_vals[trader_name] = {
                "Quantity": agg(trader.amount),  # kWh
                "Costs": agg(trader.time_step_cost),  # €
                "Emissions": agg(trader.emissions),  # kg
            }
        return trader_vals

    def _build_scenario_results_dict(
        self,
        *,
        prob: float,
        objective_kind: str,
        scen_obj_value: float,
        capex: float,
        total_emissions_t: float,
    ) -> dict[Any, Any]:
        return {
            ("scenario", "probability"): prob,
            ("objective", objective_kind): scen_obj_value,
            ("objective", "capex"): capex,
            ("emissions", "total_t"): total_emissions_t,
        }

    def _write_traders_into_results(
        self, scen_results: dict[Any, Any], trader_vals: dict[str, dict[str, float]]
    ) -> None:
        for name, v in trader_vals.items():
            scen_results[("energy", f"{name}_mwh")] = v["Quantity"] * 1e-3
            scen_results[("costs", f"{name}_keur")] = v["Costs"] * 1e-3
            scen_results[("emissions", f"{name}_t")] = v["Emissions"] * 1e-3

    def _accumulate_expected_traders(
        self, exp: _ExpectedAccumulators, trader_vals: dict[str, dict[str, float]], prob: float
    ) -> None:
        for name, v in trader_vals.items():
            exp.add_weighted(exp.energy_mwh, name, prob, v["Quantity"] * 1e-3)
            exp.add_weighted(exp.costs_keur, name, prob, v["Costs"] * 1e-3)
            exp.add_weighted(exp.emissions_t_by_trader, name, prob, v["Emissions"] * 1e-3)

    def _collect_investment_metrics(self, system: BasicSystem) -> dict[str, dict[str, float]]:
        invest_metrics: dict[str, dict[str, float]] = {}
        for inv_name, inv_unit in self._iter_investments(system):
            invest_metrics[inv_name] = self._read_investment_unit(inv_unit)
        return invest_metrics

    def _read_investment_unit(self, inv_unit) -> dict[str, float]:
        def _val(primary_getter, fallback_getter) -> float:
            try:
                return float(value(primary_getter()))
            except Exception:
                return float(value(fallback_getter()))

        y_val = _val(lambda: inv_unit.is_bought, lambda: inv_unit.model.y)
        p_nom_val = _val(lambda: inv_unit._p_out_nom, lambda: inv_unit.model.p_out_nom)
        invest_cost_val = _val(lambda: inv_unit.onetime_cost, lambda: inv_unit.model.investment_cost)

        out: dict[str, float] = {
            "bought": y_val,
            "p_out_nom": p_nom_val,
            "investment_cost": invest_cost_val,
        }

        if hasattr(inv_unit, "model") and hasattr(inv_unit.model, "p_out_nom_min"):
            out["p_out_nom_min"] = float(value(inv_unit.model.p_out_nom_min))
        if hasattr(inv_unit, "model") and hasattr(inv_unit.model, "p_out_nom_max"):
            out["p_out_nom_max"] = float(value(inv_unit.model.p_out_nom_max))

        return out

    def _write_investments_into_results(
        self, scen_results: dict[Any, Any], invest_metrics: dict[str, dict[str, float]]
    ) -> None:
        for inv_name, im in invest_metrics.items():
            scen_results[("investment", f"{inv_name}_bought")] = im["bought"]
            scen_results[("investment", f"{inv_name}_p_out_nom")] = im["p_out_nom"]
            scen_results[("investment", f"{inv_name}_investment_cost")] = im["investment_cost"]
            if "p_out_nom_min" in im:
                scen_results[("investment", f"{inv_name}_p_out_nom_min")] = im["p_out_nom_min"]
            if "p_out_nom_max" in im:
                scen_results[("investment", f"{inv_name}_p_out_nom_max")] = im["p_out_nom_max"]

    def _accumulate_expected_investments(
        self, exp: _ExpectedAccumulators, invest_metrics: dict[str, dict[str, float]], prob: float
    ) -> None:
        for inv_name, im in invest_metrics.items():
            exp.add_weighted(exp.invest_bought, inv_name, prob, im["bought"])
            exp.add_weighted(exp.invest_p_out_nom, inv_name, prob, im["p_out_nom"])
            exp.add_weighted(exp.invest_cost, inv_name, prob, im["investment_cost"])

    def _finalize_expected(self, results: dict[str, dict[Any, Any]], exp: _ExpectedAccumulators) -> None:
        expected = results["__expected__"]

        expected.update(
            {
                ("scenario", "probability_sum"): exp.prob_sum,
                ("emissions", "total_t"): exp.total_emissions_t,
                ("objective", "capex"): exp.capex,
            }
        )

        def _write_group(group: str, values: dict[str, float], *, suffix: str, scale: float, unit_suffix: str) -> None:
            for name, val in values.items():
                expected[(group, f"{name}{unit_suffix}{suffix}")] = val * scale

        def _write_invest_group(values: dict[str, float], *, metric_suffix: str, suffix: str, scale: float) -> None:
            for inv_name, val in values.items():
                expected[("investment", f"{inv_name}_{metric_suffix}{suffix}")] = val * scale

        norm = None
        if (not isnan(exp.prob_sum)) and exp.prob_sum not in (0.0, 1.0):
            norm = 1.0 / exp.prob_sum

        variants: list[tuple[str, float]] = [("", 1.0)]
        if norm is not None:
            variants.append(("_normalized", norm))

        for suffix, scale in variants:
            if suffix:
                expected[("emissions", f"total_t{suffix}")] = exp.total_emissions_t * scale
                expected[("objective", f"capex{suffix}")] = exp.capex * scale

            _write_group("energy", exp.energy_mwh, suffix=suffix, scale=scale, unit_suffix="_mwh")
            _write_group("costs", exp.costs_keur, suffix=suffix, scale=scale, unit_suffix="_keur")
            _write_group("emissions", exp.emissions_t_by_trader, suffix=suffix, scale=scale, unit_suffix="_t")

            _write_invest_group(exp.invest_bought, metric_suffix="bought", suffix=suffix, scale=scale)
            _write_invest_group(exp.invest_p_out_nom, metric_suffix="p_out_nom", suffix=suffix, scale=scale)
            _write_invest_group(exp.invest_cost, metric_suffix="investment_cost", suffix=suffix, scale=scale)

    def _collect_results(self, scenarios: ScenarioCollection, fw: RobustFramework) -> dict[str, dict[Any, Any]]:
        results: dict[str, dict[Any, Any]] = {}

        objective_kind = self.config.system.objective
        expected_value = float(fw.objective_value())

        exp = _ExpectedAccumulators()
        results["__expected__"] = {("objective", objective_kind): expected_value}

        for scen in scenarios:
            scen_name = scen.name
            system: BasicSystem = scen.system
            prob = float(getattr(scen, "probability", 0.0))
            exp.prob_sum += prob

            agg = self._make_safe_aggregator(system)

            trader_vals = self._collect_trader_vals(system, agg)
            total_emissions_t = sum(v["Emissions"] for v in trader_vals.values()) * 1e-3
            exp.total_emissions_t += prob * total_emissions_t

            scen_obj_value = float(value(system.objective))
            capex = self._total_investment_cost(system)
            exp.capex += prob * capex

            invest_metrics = self._collect_investment_metrics(system)
            self._accumulate_expected_investments(exp, invest_metrics, prob)

            scen_results = self._build_scenario_results_dict(
                prob=prob,
                objective_kind=objective_kind,
                scen_obj_value=scen_obj_value,
                capex=capex,
                total_emissions_t=total_emissions_t,
            )

            self._write_traders_into_results(scen_results, trader_vals)
            self._accumulate_expected_traders(exp, trader_vals, prob)

            self._write_investments_into_results(scen_results, invest_metrics)
            results[scen_name] = scen_results

        self._finalize_expected(results, exp)
        return results

    # -----------------------
    # Public API
    # -----------------------

    def evaluate_systems(
        self, scenarios: StochasticScenarioCollection | None = None
    ) -> tuple[dict[str, dict[Any, Any]], RobustFramework]:
        scenarios = self.scenarios if scenarios is None else scenarios

        self._attach_objectives(scenarios)
        fw = self._build_and_solve_framework(scenarios)
        results = self._collect_results(scenarios, fw)

        self._save_results(results, self.h5_file_name, fw, scenarios)
        return results, fw
