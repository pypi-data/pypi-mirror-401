from __future__ import annotations

from logging import getLogger
from typing import TYPE_CHECKING, Self

from pydantic import BaseModel, ConfigDict, Field

if TYPE_CHECKING:
    from typing import Any

log = getLogger(__name__)


class ConfigSettings(BaseModel):
    model_config = ConfigDict(extra="allow", arbitrary_types_allowed=True)
    seed: int = Field(ge=0, le=999)
    verbose: bool = Field(defaule=False)
    tee: bool = Field(default=True)
    solver: str = Field(default="gurobi")
    options: dict[str, float]
    model_export: bool

    @classmethod
    def from_dict(cls, dikt: dict[str, Any]) -> Self:
        return cls(**dikt)
