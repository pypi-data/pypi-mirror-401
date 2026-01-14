from __future__ import annotations

import logging
from collections.abc import Iterator
from json import dumps, load
from pathlib import Path
from typing import Any

import h5py
from eta_components.milp_component_library.custom_types import BasicSystem
from eta_components.milp_component_library.objectives import Emissions, NetPresentValue
from numpy import array, ndarray
from pydantic import BaseModel, ConfigDict, Field
from pyomo.core.base.block import Block
from pyomo.core.base.constraint import Constraint
from pyomo.core.base.expression import Expression
from pyomo.core.base.objective import Objective
from pyomo.core.base.param import Param
from pyomo.core.base.var import Var
from pyomo.environ import value

from eta_incerto.config.config import ConfigOptimization
from eta_incerto.envs.deterministic import DeterministicFramework
from eta_incerto.envs.scenario import ScenarioCollection
from eta_incerto.envs.utils import aggregate_for_years

logger = logging.getLogger(__name__)


class DeterministicEvaluator(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    config: ConfigOptimization = Field(..., description="Optimization config from central config.json")
    scenarios: ScenarioCollection = Field(..., description="Scenarios to evaluate deterministically")
    h5_file_name: str

    # -----------------------
    # generic time series dump
    # -----------------------

    def _is_indexed_component(self, comp: Any) -> bool:
        """
        Robust across Pyomo versions: returns True if comp is indexed.
        """
        if hasattr(comp, "is_indexed"):
            try:
                return bool(comp.is_indexed())
            except Exception:
                pass

        # fallback: try keys() once
        if hasattr(comp, "keys"):
            try:
                next(iter(comp.keys()))
                return True
            except StopIteration:
                return False
            except Exception:
                return False

        return False

    def _write_indexed_component(self, group: h5py.Group, name: str, comp: Any) -> None:
        """Store indexed component as keys + values."""
        if name in group:
            del group[name]
        cgrp = group.create_group(name)

        keys = []
        vals = []
        for k in comp:
            keys.append(repr(k))
            try:
                vals.append(float(value(comp[k])))
            except Exception:
                vals.append(float("nan"))

        cgrp.create_dataset("keys", data=array(keys, dtype="S"))
        cgrp.create_dataset("values", data=array(vals, dtype=float))

    def _write_scalar_component(self, group: h5py.Group, name: str, comp: Any) -> None:
        """Store scalar component as single value."""
        if name in group:
            del group[name]
        cgrp = group.create_group(name)
        try:
            cgrp.create_dataset("value", data=float(value(comp)))
        except Exception:
            cgrp.create_dataset("value", data=str(comp))

    def _dump_pyomo_block(self, root: h5py.Group, block: Any, prefix: str = "") -> None:
        """
        Recursively dump Vars/Params/Expressions/Constraints/Objectives from a Pyomo Block/ConcreteModel.
        Compatible with components that don't implement is_scalar().
        """
        component_types = (Var, Param, Expression, Constraint, Objective)

        for comp in block.component_objects(component_types, active=None, descend_into=True):
            comp_name = f"{prefix}{comp.name}" if prefix else comp.name
            safe_name = comp_name.replace("/", "_")

            if self._is_indexed_component(comp):
                self._write_indexed_component(root, safe_name, comp)
            else:
                self._write_scalar_component(root, safe_name, comp)

    def _dump_unit(self, dump_root: h5py.Group, unit: Any, unit_path: str) -> None:
        """
        Dump a unit:
        - If it has a Pyomo model/block (unit.model), traverse that.
        - Additionally dump direct Var/Param/... on the unit itself if they exist.
        """
        ugrp = dump_root.require_group(unit_path)

        # 1) dump unit.model if it is a Pyomo Block/ConcreteModel
        if hasattr(unit, "model") and isinstance(unit.model, Block):
            mgrp = ugrp.require_group("model")
            self._dump_pyomo_block(mgrp, unit.model)

        # 2) dump direct pyomo components attached directly on unit (common in some libs)
        for attr in dir(unit):
            if attr.startswith("_"):
                continue
            try:
                obj = getattr(unit, attr)
            except Exception:
                continue

            if isinstance(obj, Block):
                continue

            if isinstance(obj, (Var, Param, Expression, Constraint, Objective)):
                if self._is_indexed_component(obj):
                    self._write_indexed_component(ugrp, attr, obj)
                else:
                    self._write_scalar_component(ugrp, attr, obj)

    # -----------------------
    # eta-components helpers
    # -----------------------

    def _iter_traders(self, system: BasicSystem) -> Iterator[tuple[str, Any]]:
        for unit in system.units:
            if all(hasattr(unit, attr) for attr in ("amount", "time_step_cost", "emissions")):
                yield unit.name, unit

    def _iter_investments(self, system: BasicSystem) -> Iterator[tuple[str, Any]]:
        for unit in system.units:
            # A) wrapper objects
            if all(hasattr(unit, attr) for attr in ("is_bought", "onetime_cost")) and any(
                hasattr(unit, a) for a in ("_p_out_nom", "_E_nom", "_e_nom")
            ):
                # accept either _p_out_nom (HP-style) or _E_nom (storage-style)
                yield unit.name, unit
                continue

            # B) pyomo model-based objects
            if not hasattr(unit, "model"):
                continue

            m = unit.model
            if not all(hasattr(m, a) for a in ("y", "investment_cost")):
                continue

            # accept either p_out_nom (existing) OR E_nom/e_nom (storage naming)
            if any(hasattr(m, a) for a in ("p_out_nom", "P_out_nom", "E_nom", "e_nom", "E_nominal", "e_nominal")):
                yield unit.name, unit

    def _total_investment_cost(self, system: BasicSystem) -> float:
        total = 0.0
        for _, inv_unit in self._iter_investments(system):
            try:
                total += float(value(inv_unit.onetime_cost))
            except Exception:
                total += float(value(inv_unit.model.investment_cost))
        return total

    # ---------- helpers to read design variables robustly ----------

    @staticmethod
    def _get_first_attr(obj: Any, names: tuple[str, ...]) -> tuple[str | None, Any | None]:
        """Return (name, getattr(obj,name)) for the first attribute that exists, else (None, None)."""
        for n in names:
            if hasattr(obj, n):
                try:
                    return n, getattr(obj, n)
                except Exception:
                    continue
        return None, None

    def _get_design_nominal(self, unit: Any) -> tuple[str, Any]:
        """
        Return (var_name, var_obj) for the nominal design variable.

        Works with:
        - wrapper objects: unit._E_nom / unit._e_nom / unit._p_out_nom
        - model objects: unit.model.E_nom / e_nom / p_out_nom / ...
        """
        # wrapper-style first
        name, obj = self._get_first_attr(unit, ("_E_nom", "_e_nom", "_p_out_nom"))
        if obj is not None:
            return name, obj

        # pyomo model-style
        if hasattr(unit, "model"):
            name, obj = self._get_first_attr(
                unit.model,
                (
                    # preferred storage naming (your alias will provide E_nom)
                    "E_nom",
                    "e_nom",
                    "E_nominal",
                    "e_nominal",
                    # existing naming in current storage/HP models
                    "p_out_nom",
                    "P_out_nom",
                ),
            )
            if obj is not None:
                return name, obj

        raise AttributeError(f"Could not find a nominal design variable on unit '{getattr(unit, 'name', '?')}'.")

    # -----------------------
    # objective attachment + solve
    # -----------------------

    def _load_weights(self, series_file_name: str, system: BasicSystem) -> dict[int, float]:
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
            emissions_obj = Emissions(
                "emissions_objective",
                {"weights": weights},
                system,
            )

            if objective_kind == "npv":
                system.set_objective(npv_obj)
            elif objective_kind == "emissions":
                system.set_objective(emissions_obj)
            else:
                raise ValueError(f"Unknown objective_kind: {objective_kind}")

    def _build_and_solve_framework(self, scenarios: ScenarioCollection) -> DeterministicFramework:
        fw = DeterministicFramework(scenarios=scenarios)
        fw.build_model()
        fw.solve(
            solver_name=self.config.settings.solver,
            tee=self.config.settings.tee,
            options=self.config.settings.options,
            model_export=self.config.settings.model_export,
        )
        return fw

    # -----------------------
    # results collection
    # -----------------------

    def _read_investment_unit(self, inv_unit: Any) -> dict[str, float | str]:
        def _val(primary_getter, fallback_getter) -> float:
            try:
                return float(value(primary_getter()))
            except Exception:
                return float(value(fallback_getter()))

        # bought
        y_val = _val(lambda: inv_unit.is_bought, lambda: inv_unit.model.y)

        # nominal design variable (E_nom for storages)
        var_name, var_obj = self._get_design_nominal(inv_unit)
        nom_val = float(value(var_obj))

        # capex
        invest_cost_val = _val(lambda: inv_unit.onetime_cost, lambda: inv_unit.model.investment_cost)

        out: dict[str, float | str] = {
            "bought": y_val,
            "design_var_name": var_name if var_name is not None else "",
            # Unified key you can always use
            "E_nom": nom_val,
            "investment_cost": invest_cost_val,
        }

        # optional bounds (support points min/max)
        if hasattr(inv_unit, "model"):
            m = inv_unit.model
            # storage naming
            if hasattr(m, "E_nom_min"):
                out["E_nom_min"] = float(value(m.E_nom_min))
            if hasattr(m, "E_nom_max"):
                out["E_nom_max"] = float(value(m.E_nom_max))

            # your current BaseDimensioningStorage naming (misnamed but useful)
            if hasattr(m, "p_out_nom_min"):
                out["E_nom_min"] = float(value(m.p_out_nom_min))
            if hasattr(m, "p_out_nom_max"):
                out["E_nom_max"] = float(value(m.p_out_nom_max))

        return out

    def _collect_investment_metrics(self, system: BasicSystem) -> dict[str, dict[str, float | str]]:
        invest_metrics: dict[str, dict[str, float | str]] = {}
        for inv_name, inv_unit in self._iter_investments(system):
            invest_metrics[inv_name] = self._read_investment_unit(inv_unit)
        return invest_metrics

    # ---- annualization helpers ----

    @staticmethod
    def _annualize_dict(values_by_year: dict[Any, Any], scale: float) -> dict[int, float]:
        return {int(y): float(v) * scale for y, v in values_by_year.items()}

    def _collect_results(self, scenarios: ScenarioCollection, fw: DeterministicFramework) -> dict[str, dict[Any, Any]]:
        results: dict[str, dict[Any, Any]] = {}
        objective_kind = self.config.system.objective

        for scen in scenarios:
            system: BasicSystem = scen.system

            # step_length handling: if your step_length is in hours, this converts kW -> kWh
            dt_hours = float(getattr(system, "step_length", 1.0))

            energy_to_kwh = 1.0 / 1000  # Wh-->kWh

            # ---- trader totals (yearly + scalar) ----
            trader_vals_yearly: dict[str, dict[str, dict[int, float]]] = {}

            for trader_name, trader in self._iter_traders(system):
                # Energy:
                qty_w_avg_period_by_year = aggregate_for_years(trader.amount, system)  # now W (avg typical day)
                qty_wh_avg_period_by_year = {
                    int(y): float(v) * dt_hours for y, v in qty_w_avg_period_by_year.items()
                }  # Wh (avg day)
                qty_kwh_avg_period_by_year = {
                    y: v * energy_to_kwh for y, v in qty_wh_avg_period_by_year.items()
                }  # kWh (avg day)

                # multiply average day by number of days in a year
                qty_kwh_by_year = {
                    y: v * self.config.system.n_days_in_year for y, v in qty_kwh_avg_period_by_year.items()
                }

                # Costs: if time_step_cost was computed with amount assumed in kW,
                # but amount is now W -> divide by 1000 here.
                costs_avg_period_by_year = {
                    int(y): float(v) for y, v in aggregate_for_years(trader.time_step_cost, system).items()
                }
                costs_by_year = {
                    int(y): float(v) * self.config.system.n_days_in_year for y, v in costs_avg_period_by_year.items()
                }

                # Emissions: same logic if emissions were computed from amount (kW assumption)
                emissions_avg_period_by_year = {
                    int(y): float(v) for y, v in aggregate_for_years(trader.emissions, system).items()
                }
                emissions_by_year = {
                    int(y): float(v) * self.config.system.n_days_in_year
                    for y, v in emissions_avg_period_by_year.items()
                }

                trader_vals_yearly[trader_name] = {
                    "Quantity_kWh_per_year": qty_kwh_by_year,
                    "Costs_per_year": costs_by_year,
                    "Emissions_per_year": emissions_by_year,
                }

            # opex weighted, aggregated for period
            # annual cashflow components (already weighted/annualized in the objective)
            opex_avg_period_by_year = {int(y): float(value(system.objective.opex[y])) for y in system.years_set}
            opex_by_year = {
                int(y): float(v) * self.config.system.n_days_in_year for y, v in opex_avg_period_by_year.items()
            }

            # ---- classic KPI blocks ----
            obj_val = float(value(system.objective))
            capex_total = self._total_investment_cost(system)
            invest_metrics = self._collect_investment_metrics(system)

            metrics: dict[tuple[str, str], Any] = {}
            # investment KPIs
            for inv_name, im in invest_metrics.items():
                metrics[("technical", f"{inv_name}_E_nom")] = float(im["E_nom"])
                metrics[("technical", f"{inv_name}_design_var_name")] = str(im.get("design_var_name", ""))
                metrics[("economical", f"{inv_name}_capex")] = float(im["investment_cost"])
                metrics[("technical", f"{inv_name}_bought")] = float(im["bought"])

                # optional bounds if present
                if "E_nom_min" in im:
                    metrics[("technical", f"{inv_name}_E_nom_min")] = float(im["E_nom_min"])
                if "E_nom_max" in im:
                    metrics[("technical", f"{inv_name}_E_nom_max")] = float(im["E_nom_max"])

            # totals + dispatch KPIs
            metrics[("economical", "capex_total")] = capex_total
            metrics[("economical", "npv_yearly")] = obj_val
            metrics[("economical", "opex_yearly")] = opex_by_year
            metrics[("technical", "traders_yearly")] = trader_vals_yearly

            results[scen.name] = metrics
            logger.info("Scenario %s solved: %s = %.6g", scen.name, objective_kind.upper(), obj_val)

        return results

    # -----------------------
    # save results (meta + per-scenario metrics + config)
    # -----------------------

    def _save_results(
        self,
        results: dict[str, dict[Any, Any]],
        h5_file_name: str,
        fw: DeterministicFramework,
        scenarios: ScenarioCollection,
    ) -> None:
        out_dir = Path(self.config.paths.results_dir)
        out_dir.mkdir(parents=True, exist_ok=True)

        hdf_path = out_dir / h5_file_name
        if hdf_path.exists():
            hdf_path.unlink()

        def _to_hdf5_value(v: Any) -> Any:
            """
            Minimal compatibility layer for h5py:
            - dict/list/tuple -> JSON bytes (utf-8)
            - str -> utf-8 bytes
            - numpy arrays -> keep
            - scalars -> keep (or bytes fallback)
            """
            if isinstance(v, (dict, list, tuple)):
                return dumps(v).encode("utf-8")
            if isinstance(v, str):
                return v.encode("utf-8")
            if v is None:
                return b""
            return v

        with h5py.File(hdf_path, "w") as f:
            # 1) metrics per scenario
            for scen_name, metrics in results.items():
                grp = f.create_group(scen_name)
                for (category, name), v in metrics.items():
                    cat_grp = grp.require_group(category)
                    if name in cat_grp:
                        del cat_grp[name]

                    v2 = _to_hdf5_value(v)

                    try:
                        cat_grp.create_dataset(name, data=v2)
                    except TypeError:
                        cat_grp.create_dataset(name, data=str(v2))

            # 2) dump full model/unit data per scenario
            for scen in scenarios:
                scen_grp = f.require_group(scen.name)
                dump_root = scen_grp.require_group("unit_dispatch")

                system: BasicSystem = scen.system
                for unit in system.units:
                    self._dump_unit(dump_root, unit, f"units/{unit.name}")

            # 3) config (unchanged)
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
    # Public API
    # -----------------------

    def evaluate_systems(self, scenarios: ScenarioCollection | None = None) -> dict[str, dict[Any, Any]]:
        scenarios = self.scenarios if scenarios is None else scenarios

        self._attach_objectives(scenarios)
        fw = self._build_and_solve_framework(scenarios)
        results = self._collect_results(scenarios, fw)

        self._save_results(results, self.h5_file_name, fw, scenarios)
        return results
