from __future__ import annotations

import datetime
from os import PathLike
from typing import (
    Literal,
    Self,  # type: ignore[attr-defined]
    SupportsFloat,
)

from numpy import (
    floating as np_floating,
    signedinteger as np_signedinteger,
    unsignedinteger as np_unsignedinteger,
)

__all__ = [
    "FillMethod",
    "Number",
    "Path",
    "Primitive",
    "Self",
    "TimeStep",
]


# Other custom types:
Path = str | PathLike
Number = float | int | np_floating | np_signedinteger | np_unsignedinteger
TimeStep = int | float | datetime.timedelta
# str, bool, bytes explicitly defined for clarity, despite being implicitly included in SupportsFloat
Primitive = SupportsFloat | str | bool | bytes

FillMethod = Literal["ffill", "bfill", "interpolate", "asfreq"]
