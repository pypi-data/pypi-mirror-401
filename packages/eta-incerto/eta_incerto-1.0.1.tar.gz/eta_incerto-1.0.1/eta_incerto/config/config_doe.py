from __future__ import annotations

from logging import getLogger
from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict

if TYPE_CHECKING:
    pass


log = getLogger(__name__)


class ConfigDoe(BaseModel):
    model_config = ConfigDict(extra="allow", arbitrary_types_allowed=True)
    n_samples: int
    h5_filename: str
    method: str
    dist_names: str | list[str]
