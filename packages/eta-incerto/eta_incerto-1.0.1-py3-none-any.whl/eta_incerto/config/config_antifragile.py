from __future__ import annotations

from chaospy.distributions.baseclass import Distribution
from pandas import DataFrame
from pydantic import BaseModel, ConfigDict, Field

from eta_incerto.config.config import ConfigOptimization
from eta_incerto.envs.model import Model


class AntifragileConfig(BaseModel):
    """Validated input for antifragile evaluation."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    config: ConfigOptimization = Field(..., description="Optimization config from central config.json")
    model_builder: Model = Field(..., description="Model to use for evaluation")
    demand_series: DataFrame = Field(..., description="Demand to use for model")
    distribution_data: Distribution = Field(..., description="Distribution of input parameters")
    h5_file_name: str
    variable_names: str | list[str]
    objective_names: str | list[str]
