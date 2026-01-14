from __future__ import annotations

from pathlib import Path

from pandas import DataFrame, read_csv
from pydantic import BaseModel, Field, field_validator, model_validator  # <- add Field, model_validator

Index = tuple[int, int, int]  # (year, period, timestep)


class SupplierData(BaseModel):
    type: str
    unit_price: dict[Index, float]
    emissions_per_unit: dict[Index, float]


class ScenarioFile(BaseModel):
    path: Path
    name: str
    probability: float | None = Field(default=None, ge=0.0)  # <- singular + scalar

    @field_validator("path")
    @classmethod
    def check_file_exists(cls, v: Path):
        if not v.exists():
            raise ValueError(f"Scenario file not found: {v}")
        return v

    def load_dataframe(self, **kwargs) -> DataFrame:
        """Load the csv file as a DataFrame."""
        return read_csv(self.path, **kwargs)

    def load_supplier_data(self, dims, carrier_types: list[str]) -> dict[str, SupplierData]:
        """Convert fixed (two-row header) carrier_type CSV into SupplierData for all requested carriers."""
        df_supplier = self.load_dataframe(header=[0, 1]).set_index(("carrier_type", "year"))

        available = set(df_supplier.columns.get_level_values(0)) - {"carrier_type"}
        missing = set(carrier_types) - available
        if missing:
            raise KeyError(f"Missing carrier columns in {self.path.name}: {sorted(missing)}")

        out: dict[str, SupplierData] = {}

        for c in carrier_types:
            unit_price_series = df_supplier[(c, "unit_price")]
            emission_series = df_supplier[(c, "emissions_per_unit")]

            unit_price: dict[Index, float] = {}
            emission: dict[Index, float] = {}

            for year in df_supplier.index:
                up = float(unit_price_series.loc[year])
                em = float(emission_series.loc[year])

                for period in range(1, dims.n_periods + 1):
                    for timestep in range(1, dims.n_time_steps + 1):
                        idx = (int(year), period, timestep)
                        unit_price[idx] = up
                        emission[idx] = em

            out[c] = SupplierData(type=c, unit_price=unit_price, emissions_per_unit=emission)

        return out


class ConfigScenario(BaseModel):
    carrier_types: list[str]
    scenario_file: list[ScenarioFile]

    @model_validator(mode="after")
    def validate_probabilities(self):
        missing = [sf.name for sf in self.scenario_file if sf.probability is None]
        if missing:
            raise ValueError(f"Missing probability for scenarios: {missing}")

        total = sum(float(sf.probability) for sf in self.scenario_file)  # type: ignore[arg-type]
        if abs(total - 1.0) > 1e-9:
            raise ValueError(f"Probabilities must sum to 1.0, got {total}")

        return self

    def as_supplier_data(self, dims, carrier_types) -> dict[str, SupplierData]:
        """Load all scenario files as structured SupplierData objects"""
        return {sf.name: sf.load_supplier_data(dims, carrier_types) for sf in self.scenario_file}
