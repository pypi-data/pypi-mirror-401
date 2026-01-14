from __future__ import annotations

import logging
import warnings
from collections.abc import Iterable
from typing import Any

from pydantic import BaseModel

logger = logging.getLogger(__name__)


class Scenario(BaseModel):
    """Data container. Stores data and not behavior. Pydantic used to avoid boilerplate code.
    A Scenario is a built system with a name. BasicSystem here is a type, defined in the eta-components
    library mcl.
    """

    # TODO @MFr(#2): Enhance type checking, as currently Any is allowing all system types

    model_config = {"arbitrary_types_allowed": True}

    name: str
    system: Any  # in combination with eta-components: from eta_components.milp_component_library.
    # custom_types import BasicSystem, for more general usage Anyhere
    series: Any = None
    energy_scenario: Any = None
    series_file_name: str = ""
    # TODO @MFr(#1): Adapt types for series and scenario in config to enable type checking here?


class ScenarioCollection:
    """Manages multiple scenario objects. Has methods to define scenarios in the
    collection (set_scenario) and receive scenarios (get_scenario).
    """

    _scenario_type = Scenario

    def __init__(self, scenarios: Iterable[_scenario_type] | None = None):
        self._scenarios: dict[str, Scenario] = {}
        if scenarios is not None:
            for scenario in scenarios:
                self.set_scenario(scenario)

    def __iter__(self):
        """Enables iterating over the objects directly."""
        return iter(self._scenarios.values())

    def set_scenario(self, scenario: _scenario_type):
        if scenario.name in self._scenarios:
            warnings.warn(f"Overwriting scenario {scenario.name}.", stacklevel=2)
        self._scenarios[scenario.name] = scenario

    def get_scenario(self, name: str) -> _scenario_type:
        if name not in self._scenarios:
            raise KeyError(f"No scenario of name {name}.")
        return self._scenarios[name]

    def names(self) -> dict.keys:
        return self._scenarios.keys()
