from __future__ import annotations

from importlib import import_module
from logging import getLogger
from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field, field_validator
from pymoo.core.algorithm import Algorithm
from pymoo.core.crossover import Crossover
from pymoo.core.mutation import Mutation
from pymoo.core.sampling import Sampling
from pymoo.core.selection import Selection
from pymoo.operators.selection.tournament import TournamentSelection

from .registry import DIKT_PATH, REGISTRY_MAP

if TYPE_CHECKING:
    from typing import Any


log = getLogger(__name__)


class ConfigAlgorithm(BaseModel):
    model_config = ConfigDict(extra="allow", arbitrary_types_allowed=True)
    algorithm: str = Field(..., description="Algorithm name, e.g., 'NSGA2'", alias="name")
    algorithm_class: Algorithm = Field(None, exclude=True)
    pop_size: int = Field(gt=0)
    sampling: str
    sampling_class: Sampling = Field(None, exclude=True)
    selection: str
    selection_class: Selection = Field(None, exclude=True)
    crossover: str
    crossover_class: Crossover = Field(None, exclude=True)
    mutation: str
    mutation_class: Mutation = Field(None, exclude=True)

    @field_validator("algorithm", "sampling", "selection", "crossover", "mutation", mode="before")
    @classmethod
    def format_operators_class(cls, input_str, info):
        """
        Dynamically imports and instantiates an operator class based on its name.

        Works for fields: 'algorithm', 'sampling', 'selection', 'crossover', 'mutation'.
        Supports:
        - Full module path: "pymoo.operators.sampling.rnd.FloatRandomSampling"
        - Short operator name: "FloatRandomSampling", "SBX", etc.
        Returns
        """
        field_name = info.field_name
        registry = REGISTRY_MAP[field_name]

        if not isinstance(input_str, str):
            raise ValueError(f"Expected a string for '{field_name}', got {type(input_str).__name__}")

        is_algorithm = field_name.startswith("algorithm")

        # normalize only for algorithm field
        normalized_str = input_str.upper().replace("-", "") if field_name.startswith("algorithm") else input_str

        # determine base module dynamically
        base_module = DIKT_PATH["algorithm"] if field_name.startswith("algorithm") else DIKT_PATH["parameters"]

        def get_alias(name: str) -> str:
            """Return alias from registry or raise error if not found."""
            if is_algorithm:
                return registry.get(name, name.lower())
            try:
                return next(k for k, v in registry.items() if name in v)
            except StopIteration:
                error_msg = f"Unknown value '{name}' in {field_name.upper()} registry."
                log.error(error_msg)
                raise ValueError(error_msg) from None

        # --- Case 1: full module path ---
        if "." in normalized_str:
            module_path, class_name = normalized_str.rsplit(".", 1)
            alias = get_alias(class_name)
            expected_module_path = (
                f"{base_module}.{field_name}.{alias}" if not is_algorithm else f"{base_module}.{alias}.{normalized_str}"
            )
            if not module_path.startswith(expected_module_path):
                error_msg = f"Module path '{module_path}' does not match expected '{expected_module_path}'"
                log.error(error_msg)
                raise ValueError(error_msg)
            return normalized_str

        # --- Case 2: short input name ---
        alias = get_alias(normalized_str)

        # build full path dynamically
        return (
            f"{base_module}.{field_name}.{alias}.{normalized_str}"
            if not is_algorithm
            else f"{base_module}.{alias}.{normalized_str}"
        )

    def model_post_init(self, context: Any) -> None:
        def load_class(path: str, name: str):
            try:
                module, cls_name = path.rsplit(".", 1)
                return getattr(import_module(module), cls_name)
            except ModuleNotFoundError:
                log.error("Module %s not found for %s.", module, name)
                raise
            except AttributeError:
                log.error("Class %s not found in module %s for %s.", cls_name, module, name)
                raise

        self.algorithm_class = load_class(self.algorithm, "algorithm")
        self.sampling_class = load_class(self.sampling, "sampling")
        self.selection_class = load_class(self.selection, "selection")
        self.crossover_class = load_class(self.crossover, "crossover")
        self.mutation_class = load_class(self.mutation, "mutation")

        # --- Inject custom comparator for NSGA-II tournament ---
        if self.selection_class.__name__ == "TournamentSelection":
            from eta_incerto.util.nsga2_tournament import nsga2_tournament

            self.selection_class = lambda **kwargs: TournamentSelection(func_comp=nsga2_tournament)

        # Log a clear summary of loaded classes
        log.info(
            "Successfully loaded algorithm and operator classes:\n"
            "Algorithm: %s\n"
            "Sampling: %s\n"
            "Selection: %s\n"
            "Crossover: %s\n"
            "Mutation: %s",
            self.algorithm_class.__name__,
            self.sampling_class.__name__,
            self.selection_class.__name__,
            self.crossover_class.__name__,
            self.mutation_class.__name__,
        )
