from __future__ import annotations

from logging import getLogger
from pathlib import Path
from typing import TYPE_CHECKING

from pydantic import BaseModel, Field, ValidationError, field_validator

from eta_incerto.config.config_algorithm import ConfigAlgorithm
from eta_incerto.config.config_analysis import ConfigAnalysis
from eta_incerto.config.config_doe import ConfigDoe
from eta_incerto.config.config_evaluate import ConfigEvaluate
from eta_incerto.config.config_paths import ConfigPaths
from eta_incerto.config.config_pcetest import ConfigPceTest
from eta_incerto.config.config_plotting import ConfigPlotting
from eta_incerto.config.config_problem import ConfigProblem
from eta_incerto.config.config_scenario import ConfigScenario
from eta_incerto.config.config_series import ConfigSeries
from eta_incerto.config.config_settings import ConfigSettings
from eta_incerto.config.config_system import ConfigSystem
from eta_incerto.config.config_termination import ConfigTermination
from eta_incerto.util.io_utils import load_config

if TYPE_CHECKING:
    from typing import Any


log = getLogger(__name__)


class ConfigOptimization(BaseModel):
    """Configuration for the optimization, which can be loaded from a JSON file."""

    config_name: str
    root_path: Path = Field(frozen=True)
    paths: ConfigPaths
    series: ConfigSeries
    scenario: ConfigScenario
    settings: ConfigSettings
    system: ConfigSystem
    problem: ConfigProblem
    termination: ConfigTermination
    algorithm: ConfigAlgorithm
    evaluate: ConfigEvaluate
    plotting: ConfigPlotting
    doe: ConfigDoe
    pcetest: ConfigPceTest
    analysis: ConfigAnalysis = Field(default_factory=ConfigAnalysis)

    @field_validator("root_path", mode="before")
    @classmethod
    def convert_to_path(cls, v) -> Path:
        if isinstance(v, str):
            return Path(v)
        return v

    @classmethod
    def from_file(cls, file: Path, root_path: Path) -> ConfigOptimization:
        """Load configuration from JSON/TOML/YAML file, which consists of the following sections:

        :param file: Path to the configuration file.
        :param overwrite: Config parameters to overwrite.
        :return: Config object.
        """
        config = load_config(file)
        config_name = Path(file).stem

        return ConfigOptimization.from_dict(config, config_name, root_path)

    @classmethod
    def from_dict(cls, config: dict[str, Any], config_name: str, root_path: Path) -> ConfigOptimization:
        """Build a Config object from a dictionary of configuration options.

        :param config: Dictionary of configuration options.
        :param file: Path to the configuration file.
        :param root_path: Root path for the optimization configuration run.
        :return: Config object.
        """

        # Required sections
        required = {"settings", "paths", "system", "scenario", "series"}
        # Use set difference to find missing sections
        missing = required - config.keys()  # O(n) set operation
        if missing:
            # Raise immediately if any missing
            raise ValueError(f"Missing section(s) {', '.join(missing)} in configuration file {config_name}.")

        def _pop_dict(dikt: dict[str, Any], key: str) -> dict[str, Any]:
            val = dikt.pop(key)
            if not isinstance(val, dict):
                msg = f"'{key}' section must be a dictionary of settings."
                raise TypeError(msg)
            return val

        def _load_section(dikt: dict[str, Any], key: str, cls_: type, extra: dict | None = None) -> Any:
            """Pop a section and load it into a Pydantic model."""
            section_dict = _pop_dict(dikt, key)

            if extra:
                section_dict.update(extra)

            try:
                return cls_.model_validate(section_dict)
            except ValidationError as e:
                log.info(e.json())
                log.exception("Failed reading '%s' section from config %s.", key, config_name)
                raise

        # Load required sections
        series = _load_section(config, "series", ConfigSeries, extra={"root_path": root_path})
        scenario = _load_section(config, "scenario", ConfigScenario, extra={"root_path": root_path})
        settings = _load_section(config, "settings", ConfigSettings)
        paths = _load_section(config, "paths", ConfigPaths, extra={"root_path": root_path})
        system = _load_section(config, "system", ConfigSystem)
        problem = _load_section(config, "problem", ConfigProblem)
        termination = _load_section(config, "termination", ConfigTermination)
        algorithm = _load_section(config, "algorithm", ConfigAlgorithm)
        evaluate = _load_section(config, "evaluate", ConfigEvaluate)
        plotting = _load_section(config, "plotting", ConfigPlotting)
        doe = _load_section(config, "doe", ConfigDoe)
        pcetest = _load_section(config, "pcetest", ConfigPceTest)

        analysis = _load_section(config, "analysis", ConfigAnalysis) if "analysis" in config else ConfigAnalysis()

        return cls(
            config_name=config_name,
            root_path=root_path,
            paths=paths,
            series=series,
            settings=settings,
            system=system,
            scenario=scenario,
            problem=problem,
            termination=termination,
            algorithm=algorithm,
            evaluate=evaluate,
            plotting=plotting,
            doe=doe,
            pcetest=pcetest,
            analysis=analysis,
        )
