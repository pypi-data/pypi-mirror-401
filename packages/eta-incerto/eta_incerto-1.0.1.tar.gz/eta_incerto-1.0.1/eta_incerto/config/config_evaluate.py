from __future__ import annotations

from logging import getLogger

from pydantic import BaseModel, ConfigDict

log = getLogger(__name__)


class ConfigEvaluate(BaseModel):
    model_config = ConfigDict(extra="allow", arbitrary_types_allowed=True)

    name: str
    pce_order: int
    pce_rule: str
    quad_order: int
    quad_rule: str
    stat_n_mc: int
    stat_omega: float
    stat_rule: str
    n_jobs: int
    backend: str
