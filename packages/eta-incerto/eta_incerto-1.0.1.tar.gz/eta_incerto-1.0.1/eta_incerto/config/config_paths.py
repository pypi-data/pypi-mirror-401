from __future__ import annotations

from logging import getLogger
from pathlib import Path
from typing import TYPE_CHECKING, Self

from pydantic import BaseModel, ConfigDict, Field, field_validator

if TYPE_CHECKING:
    from typing import Any

log = getLogger(__name__)


class ConfigPaths(BaseModel):
    model_config = ConfigDict(extra="allow", arbitrary_types_allowed=True)
    root_path: Path = Field(frozen=True)
    results_dir: Path | None = Field(default=None, validate_default=True)
    scenario_dir: Path = Field(default=None, validate_default=True)
    series_dir: Path | None = Field(default=None, validate_default=True)
    plots_dir: Path | None = Field(default=None, validate_default=True)
    system_dir: Path | None = Field(default=None, validate_default=True)

    @staticmethod
    def _resolve_dir(v: Path | None, root_path: Path, default: str, create: bool) -> Path:
        dir_path = Path(v) if v is not None else Path(default)
        resolved = dir_path if dir_path.is_absolute() else root_path / dir_path

        if not resolved.exists():
            if create:
                log.debug("Path %s doesn't exist. Creating directories...", resolved)
                resolved.mkdir(parents=True, exist_ok=True)
                log.info("Directories created: %s", resolved)
            else:
                raise ValueError(f"Path does not exist: {resolved}")

        if not resolved.is_dir():
            raise ValueError(f"{resolved} is not a folder")

        return resolved

    @field_validator("scenario_dir", mode="before")
    @classmethod
    def check_scenario_dir_exists(cls, v: Path | None, info) -> Path:
        """Validate that the given path exists and is a directory."""
        return cls._resolve_dir(v, info.data.get("root_path"), "scenario", create=False)

    @field_validator("results_dir", mode="before")
    @classmethod
    def create_results_dir_if_missing(cls, v: Path | None, info) -> Path:
        return cls._resolve_dir(v, info.data.get("root_path"), "results", create=True)

    @field_validator("series_dir", mode="before")
    @classmethod
    def create_series_dir_if_missing(cls, v: Path | None, info) -> Path:
        return cls._resolve_dir(v, info.data.get("root_path"), "series", create=True)

    @field_validator("system_dir", mode="before")
    @classmethod
    def create_system_dir_if_missing(cls, v: Path | None, info) -> Path:
        return cls._resolve_dir(v, info.data.get("root_path"), "systems", create=True)

    @field_validator("plots_dir", mode="before")
    @classmethod
    def create_plots_dir_if_missing(cls, v: Path | None, info) -> Path:
        return cls._resolve_dir(v, info.data.get("root_path"), "plots", create=True)

    @classmethod
    def from_dict(cls, dikt: dict[str, Any]) -> Self:
        return cls(**dikt)
