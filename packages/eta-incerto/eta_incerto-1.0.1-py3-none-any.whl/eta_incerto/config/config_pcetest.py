from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class ConfigPceTest(BaseModel):
    model_config = ConfigDict(extra="allow", arbitrary_types_allowed=True)
    sampler: str
    n_val: int
    max_order: int
    design_var_min: int
    design_var_max: int
    design_var_step: int
