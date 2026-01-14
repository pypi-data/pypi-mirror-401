"""
Analysis configuration.

This config defines optional post-processing and sensitivity analyses
(e.g. std_target analysis based on typical periods).

All values must be provided via the JSON configuration.
No defaults are defined here.
"""

from pydantic import BaseModel, Field


class ConfigAnalysis(BaseModel):
    """
    Configuration for analysis module.
    """

    enabled: bool = Field(..., description="Enable or disable the analysis module.")

    mode: str = Field(..., description="Analysis mode identifier (e.g. 'std_target').")

    factors: list[float] = Field(..., description="Scaling factors applied in the analysis.")

    seed: int = Field(..., description="Random seed used for the analysis.")

    results_subdir: str = Field(..., description="Subdirectory name for analysis results.")

    make_plots: bool = Field(..., description="Whether plots should be generated.")

    pdf_name: str = Field(..., description="Filename of the generated analysis PDF report.")
