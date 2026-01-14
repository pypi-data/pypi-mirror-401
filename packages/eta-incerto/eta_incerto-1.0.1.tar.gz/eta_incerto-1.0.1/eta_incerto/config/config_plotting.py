from __future__ import annotations

from logging import getLogger
from typing import Any

from pydantic import BaseModel, ConfigDict

log = getLogger(__name__)


class ConfigSubplot(BaseModel):
    model_config = ConfigDict(extra="allow")

    x: str
    y: str
    subplot: int
    xlabel: str | None = None
    ylabel: str | None = None
    title: str | None = None


class ConfigPlotting(BaseModel):
    model_config = ConfigDict(extra="allow", arbitrary_types_allowed=True)

    fig_w_in: float
    fig_h_in: float
    rcparams: dict[str, Any]
    subplots: list[ConfigSubplot]
    dist_names: str | list[str]
