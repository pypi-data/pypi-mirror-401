from __future__ import annotations

from logging import getLogger
from typing import TYPE_CHECKING

from numpy import (
    array,
    ndarray as np_ndarray,
)
from pydantic import BaseModel, ConfigDict, Field, field_validator

if TYPE_CHECKING:
    from typing import Any


log = getLogger(__name__)


class ConfigProblem(BaseModel):
    model_config = ConfigDict(extra="allow", arbitrary_types_allowed=True)

    n_variables: int = Field(ge=0, le=100)
    variable_names: str | list[str]

    n_objectives: int = Field(ge=0, le=3)
    objective_names: str | list[str]

    n_ieq_constraints: int = Field(ge=0, le=1, default=0)

    n_eq_constraints: int = Field(ge=0, le=1, default=0)

    obj_min: list[int | float]
    obj_max: list[int | float]

    x_lower_bound: int | float | list[float] | np_ndarray
    x_upper_bound: int | float | list[float] | np_ndarray

    @field_validator("x_lower_bound", "x_upper_bound", mode="before")
    @classmethod
    def ensure_array(cls, v):
        if isinstance(v, list):
            arr = array(v, dtype=float)
        elif isinstance(v, (int, float)):
            arr = array([v], dtype=float)
        elif isinstance(v, np_ndarray):
            arr = v.astype(float)
        else:
            raise TypeError(f"Invalid type for bounds: {type(v)}")

        # validate element-wise non-negativity
        if any(arr < 0):
            raise ValueError("Bounds must be non-negative.")
        return arr

    normalize: bool

    vtype: type = Field(
        int,  # default
        description="Type hint: either int or float for the variable to be optimized",
    )

    @field_validator("vtype", mode="before")
    @classmethod
    def parse_vtype(cls, v):
        type_map = {"int": int, "float": float}
        if isinstance(v, str):
            return type_map.get(v.lower(), int)  # default int bei unbekanntem String
        return v

    def model_post_init(self, context: Any) -> None:
        """Post-initialization hook called after model creation and validation."""
        log.info("ConfigProblem successfully initialized.")
