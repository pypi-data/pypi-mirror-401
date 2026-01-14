from __future__ import annotations

from datetime import timedelta
from logging import getLogger
from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field, field_validator
from pymoo.core.termination import Termination
from pymoo.termination import get_termination

if TYPE_CHECKING:
    from typing import Any


log = getLogger(__name__)

TERMINATION_DIKT = {
    ("N_EVAL", "n_eval", "eval", "EVAL"): "n_eval",
    ("N_GEN", "n_gen", "gen", "GEN", "Generations", "generations"): "n_gen",
    ("Time", "time"): "time",
}


class ConfigTermination(BaseModel):
    model_config = ConfigDict(extra="allow", arbitrary_types_allowed=True)

    method: str
    value: int
    termination_instance: Termination = Field(None, exclude=True)

    @field_validator("method", mode="after")
    @classmethod
    def check_method(cls, v):
        # iterate through all termination-tuples and check if v matches one of them
        for keys, normalized in TERMINATION_DIKT.items():
            if v in keys:
                return normalized
        error_msg = (
            f"Invalid termination method '{v}' for field 'method'. "
            f"Allowed methods are: {list(TERMINATION_DIKT.values())}."
        )
        log.error(error_msg)
        raise ValueError(error_msg)

    def model_post_init(self, context: Any) -> None:
        """Post-initialization hook called after model creation and validation."""

        value = str(timedelta(seconds=self.value)).rjust(8, "0") if self.method.startswith("time") else self.value
        self.termination_instance = get_termination(self.method, value)
        log.info("Termination class for %s and value %s was successfully initialized.", self.method, value)
