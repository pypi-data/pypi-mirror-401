from __future__ import annotations

import logging
from typing import Any

from pydantic import BaseModel, ConfigDict

logger = logging.getLogger(__name__)


class Model(BaseModel):
    """Data container. Stores data and not behavior. Pydantic used to avoid boilerplate code.
    A component is a stochastic uncertainty.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    config: Any | None = None
    investment_data: Any | None = None
    static_data: Any | None = None
