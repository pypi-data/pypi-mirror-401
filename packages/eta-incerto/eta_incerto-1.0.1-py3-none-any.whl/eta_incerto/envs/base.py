from __future__ import annotations

import abc
import logging
from abc import ABC
from pathlib import Path

import pyomo.environ as pyo

from eta_incerto.envs.scenario import ScenarioCollection

logger = logging.getLogger(__name__)


class UncertaintyFramework(ABC):
    def __init__(self, scenarios: ScenarioCollection):
        self._scenarios: ScenarioCollection = scenarios
        self._first_stage_variables: dict = {}
        self._global_model: pyo.ConcreteModel = pyo.ConcreteModel()

    @abc.abstractmethod
    def build_model(self):
        """Method that has to be instantiated by every instance of UncertaintyFramework."""

    def solve(
        self, solver_name: str = "gurobi", tee: bool = False, options: dict | None = None, model_export: bool = False
    ):
        if options is None:
            options = {}

        # Export BEFORE solve so we still get the LP even if infeasible / solver errors
        if model_export:
            self._global_model.write(
                "model.lp",
                io_options={"symbolic_solver_labels": True},
            )
            with Path.open("model.pprint.txt", "w", encoding="utf-8") as f:
                self._global_model.pprint(ostream=f)

        solver = pyo.SolverFactory(solver_name)
        if options:
            solver.options.update(options)
        return solver.solve(self._global_model, tee=tee)

    def _equate_investment_decisions_across_submodels(
        self, global_model: pyo.ConcreteModel, scenarios_block: pyo.Block
    ):
        submodel_first_stage_variables = self._extract_first_stage_variables_from_submodels()

        self._check_all_submodels_have_same_first_stage_variables(submodel_first_stage_variables)

        self._first_stage_variables = self._create_global_first_stage_variables(
            global_model, submodel_first_stage_variables
        )

        self._equate_global_first_stage_variables_to_submodel_first_stage_variables(
            scenarios_block, self._first_stage_variables, submodel_first_stage_variables
        )
        logger.info("Equated the investment decisions across all base scenarios.")

    def _extract_first_stage_variables_from_submodels(self):
        # TODO(#1): Add p_out_nom for all unit classes (storage and HEX)
        submodel_first_stage_variables = {}
        for scenario_name in self._scenarios.names():
            submodel_first_stage_variables[scenario_name] = {
                f"{unit.name}.{unit.model.p_out_nom.local_name}": unit.model.p_out_nom
                for unit in self._scenarios.get_scenario(scenario_name).system.units
                if unit.has_investment_decision()
            }
        return submodel_first_stage_variables

    def _check_all_submodels_have_same_first_stage_variables(
        self, submodel_first_stage_variables: dict[str, dict[str, pyo.Var]]
    ):
        first_scenario_name = self.__name_of_first_scenario()
        for scenario_name in self._scenarios.names():
            if (
                not submodel_first_stage_variables[first_scenario_name].keys()
                == submodel_first_stage_variables[scenario_name].keys()
            ):
                raise ValueError(
                    "The names of the units with investment decision must be the same for all scenarios."
                    f"For scenario {first_scenario_name} there were the units:\n"
                    f"{submodel_first_stage_variables[first_scenario_name]}.\n"
                    f"For scenario {scenario_name} there were the units:\n"
                    f"{submodel_first_stage_variables[scenario_name]}"
                )

    def __name_of_first_scenario(self):
        return next(iter(self._scenarios.names()))

    def _create_global_first_stage_variables(
        self, global_model: pyo.Model, submodel_first_stage_variables: dict[str, dict[str, pyo.Var]]
    ) -> dict[str, pyo.Var]:
        global_first_stage_variables = {}
        first_scenario_name = self.__name_of_first_scenario()
        global_model.first_stage_variables = pyo.Block()
        for var_name, _p_out_nom in submodel_first_stage_variables[first_scenario_name].items():
            var = pyo.Var(within=pyo.Reals)
            global_first_stage_variables[var_name] = var
            global_model.first_stage_variables.add_component(var_name, var)
        return global_first_stage_variables

    def _equate_global_first_stage_variables_to_submodel_first_stage_variables(
        self,
        scenarios_block: pyo.Block,
        global_first_stage_variables: dict[str, pyo.Var],
        submodel_first_stage_variables: dict[str, dict[str, pyo.Var]],
    ):
        for scenario_name in self._scenarios.names():
            scenario_block: pyo.Block = getattr(scenarios_block, scenario_name)

            # for each first-stage var in this scenario...
            for var_name, sub_var in submodel_first_stage_variables[scenario_name].items():
                # pick out the matching global var by key
                glob_var = global_first_stage_variables[var_name]

                # define one constraint per var
                c = pyo.Constraint(expr=sub_var == glob_var)
                scenario_block.add_component(f"constrain_investment_decision_of_{var_name}", c)

    def root_solution(self) -> dict[str, float]:
        first_stage_result = {}
        for var_name, var in self._first_stage_variables.items():
            first_stage_result[var_name] = pyo.value(var)
        return first_stage_result

    def graph_representation(self) -> dict[str, list[tuple[str, str]]]:
        """Returns a dictionary representing

        Returns:
            dict[str, float]: Dictionary with "nodes" and "edges".a
        """
        nodes = self._get_nodes()
        edges = self._get_edges()
        return {"nodes": nodes, "edges": edges}

    def _reference_system(self):
        """Use the first scenario's system as topology reference."""
        first_name = next(iter(self._scenarios.names()))
        return self._scenarios.get_scenario(first_name).system

    @property
    def units(self):
        return self._reference_system().units

    @property
    def networks(self):
        return self._reference_system().networks

    @property
    def environments(self):
        return self._reference_system().environments

    def _get_nodes(self) -> list[str]:
        """Returns all nodes of the graph."""
        nodes = [unit.name for unit in self.units]
        nodes += [net.name for net in self.networks]
        nodes += [env.name for env in self.environments]
        return nodes

    def _get_edges(self) -> list[dict[str, str]]:
        edges: list[dict[str, str]] = []

        # 1) Unit -><- Network edges with direction from network semantics
        for net in self.networks:
            for unit, power in net._producers:
                edges.append({"source": unit.name, "target": net.name, "kind": "producer", "power": power.local_name})
            for unit, power in net._consumers:
                edges.append({"source": net.name, "target": unit.name, "kind": "consumer", "power": power.local_name})
            for unit, power in net._prosumers:
                edges.append({"source": unit.name, "target": net.name, "kind": "prosumer", "power": power.local_name})
                edges.append({"source": net.name, "target": unit.name, "kind": "prosumer", "power": power.local_name})

        # 2) Environment -> Unit edges (dependency direction)
        env_by_id = {id(e): e for e in self.environments}
        env_by_name = {e.name: e for e in self.environments}

        for unit in self.units:
            # Look for env references on the unit instance
            for attr in dir(unit):
                # common internal naming patterns in eta-components:
                # _ambient_env, _environment, ambient_environment, environment, env, ...
                if "env" not in attr.lower():
                    continue

                obj = getattr(unit, attr, None)
                if obj is None:
                    continue

                # match by identity (best) or by name (fallback)
                env = None
                if id(obj) in env_by_id:
                    env = env_by_id[id(obj)]
                elif getattr(obj, "name", None) in env_by_name:
                    env = env_by_name[obj.name]

                if env is None:
                    continue

                edges.append(
                    {
                        "source": env.name,
                        "target": unit.name,
                        "kind": "environment",
                        "power": attr,  # reuse field as "via"/attr for traceability
                    }
                )

        return edges
