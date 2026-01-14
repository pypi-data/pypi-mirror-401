from __future__ import annotations

from logging import getLogger
from typing import TYPE_CHECKING, Self

from pydantic import BaseModel, ConfigDict, Field, ValidationInfo, field_validator

if TYPE_CHECKING:
    from typing import Any

log = getLogger(__name__)


class ConfigSystem(BaseModel):
    model_config = ConfigDict(extra="allow", arbitrary_types_allowed=True)
    variant: list[str]
    objective: str
    interest: float
    lifetime: int
    emission_cost: float
    n_years: int
    n_time_steps: int
    year_length: int = Field(int, description="Check if year_length is smaller than overall n_years.")
    n_days_in_year: int
    n_periods: int
    remove_plr: bool
    remove_storage_binary: bool

    @field_validator("year_length", mode="before")
    @classmethod
    def check_year_length(cls, year_length: int, info: ValidationInfo):
        n_years = info.data.get("n_years")
        if year_length > n_years:
            raise {"With %s, year length is bigger than number of years with %s", year_length, n_years}
        return year_length

    @classmethod
    def from_dict(cls, dikt: dict[str, Any]) -> Self:
        return cls(**dikt)
