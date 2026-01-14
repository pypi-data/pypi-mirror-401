from __future__ import annotations

from pyomo.environ import Block, ConcreteModel

from eta_incerto.envs.base import ScenarioCollection


class DeterministicFramework:
    def __init__(self, scenarios: ScenarioCollection):
        self._scenarios = scenarios
        self._global_model = None

    def build_model(self):
        self._global_model = global_model = ConcreteModel()
        global_model.scenarios = Block()

        for scenario_name in self._scenarios.names():
            scenario = self._scenarios.get_scenario(scenario_name)
            scenario.system.join_models()
            scenario.system.objective.construct_objective()

            global_model.scenarios.add_component(scenario_name, Block())
            global_model.scenarios.component(scenario_name).add_component("submodel", scenario.system.model)

    def solve(
        self,
        solver_name: str,
        tee: bool = False,
        options: dict | None = None,
        model_export: bool = False,
    ):
        """
        Solve each scenario using scenario.system.solve(), so you can export LP + pprint
        and get symbolic labels easily.

        - solver_name: e.g. "cplex" or "gurobi"
        - tee: verbose solver output
        - options: passed into system.solve(); supports 'keepfiles' and 'warmstart'
        - model_export: if True, triggers LP + pprint export inside system.solve()
        """
        if options is None:
            options = {}

        results_by_scenario = {}

        for scenario_name in self._scenarios.names():
            scenario = self._scenarios.get_scenario(scenario_name)

            res = scenario.system.solve(
                solver=solver_name,
                tee=tee,
                options=dict(options),  # copy so pops don't affect other scenarios
                model_export=model_export,
            )

            results_by_scenario[scenario_name] = res

        return results_by_scenario
