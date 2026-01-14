from __future__ import annotations

from json import load
from logging import getLogger
from pathlib import Path

from numpy import arange
from pandas import read_csv
from pydantic import BaseModel

from eta_incerto.periods.data_to_periods import TypicalData

log = getLogger(__name__)


class Dims(BaseModel):
    n_years: int
    n_periods: int
    n_time_steps: int
    step_length: int
    year_length: int


def replace_pfr_plr_bpts_with_linear_correlation(data: dict):
    for data_unit in data.values():
        if "pfr_plr_bpts" in data_unit:
            data_unit["pfr_plr_bpts"] = [[0, 0], [1, 1]]


def allow_simultaneous_charging_and_discharging_of_storages(data: dict):
    for name, data_unit in data.items():
        if "storage" in name:
            data_unit["allow_simultaneous_charging_and_discharging"] = True


def extend_to_years_index(data: dict, dims: Dims):
    for key, value in data.items():
        if isinstance(value, dict):
            value_temp = {}
            for key2, value2 in value.items():
                for year in arange(1, dims.n_years * dims.year_length + 1, dims.year_length):
                    value_temp[(year, *key2)] = value2
            data[key] = value_temp
    return data


class ConfigData(BaseModel):
    """Data configuration of the optimization run."""

    @classmethod
    def _init_typical(cls, config, root_path):
        cls.typical = TypicalData(config, root_path)

    @classmethod
    def load_file(cls, file: Path, path_root: Path) -> dict:
        _path_root: Path = Path(path_root)
        config = cls._load_config_file(file)

        for section in ("setup", "paths", "settings", "series_specific", "scenario_specific", "investment_specific"):
            if section not in config:
                msg = f"The section '{section}' is not present in configuration file {file}."
                raise ValueError(msg)

        dims = Dims(
            step_length=config["series_specific"]["step_length"],
            n_periods=config["series_specific"]["n_periods"],
            n_time_steps=config["scenario_specific"]["n_time_steps"],
            n_years=config["scenario_specific"]["n_years"],
            year_length=config["scenario_specific"]["year_length"],
        )

        data = {
            "setup": config["setup"],
            "paths": config["paths"],
            "settings": config["settings"],
            "scenario_specific": config["scenario_specific"],
            "series_specific": config["series_specific"],
            "investment_specific": config["investment_specific"],
        }

        data.update(cls.load_data(config, dims, _path_root))

        return data

    @classmethod
    def _load_energy_supplier_data(cls, config, _path_root, dims: Dims):
        """electricity_supplier_surcharge is the grid tax that gets added onto the electricity market price when taking
        electricity out of the grid. Default is 100%, approximated through:
        https://www.bmwk.de/Redaktion/DE/Artikel/Energie/strompreise-bestandteile.html

        When feeding electricity into the network, the electricity market price is paid to the IES.
        """
        file_path = Path(_path_root) / config["paths"]["relpath_scenarios"]
        csv_path = Path(file_path) / "e.csv"
        energy_trends = read_csv(csv_path, index_col=0, header=[0, 1])
        energy_trends = energy_trends.iloc[0 :: dims.year_length, :]

        data = {}
        data["electricity_supplier"] = el_supplier = {}
        el_supplier["unit_price"] = {}
        el_supplier["emissions_per_unit"] = {}
        data["electricity_feed_in"] = el_feed_in = {}
        el_feed_in["unit_price"] = {}
        el_feed_in["emissions_per_unit"] = {}
        data["gas_supplier"] = gas_supplier = {}
        gas_supplier["unit_price"] = {}
        gas_supplier["emissions_per_unit"] = {}
        data["h2_supplier"] = h2_supplier = {}
        h2_supplier["unit_price"] = {}
        h2_supplier["emissions_per_unit"] = {}

        for year in arange(1, dims.n_years * dims.year_length + 1, dims.year_length):
            for period in arange(1, dims.n_periods + 1):
                for time_step in range(1, dims.n_time_steps + 1):
                    idx = (year, period, time_step)

                    el_supplier["unit_price"][idx] = energy_trends.loc[year, ("electricity", "unit_price")]
                    el_supplier["emissions_per_unit"][idx] = energy_trends.loc[
                        year, ("electricity", "emissions_per_unit")
                    ]

                    el_feed_in["unit_price"][idx] = energy_trends.loc[year, ("electricity", "unit_price")]
                    el_feed_in["emissions_per_unit"][idx] = energy_trends.loc[
                        year, ("electricity", "emissions_per_unit")
                    ]

                    gas_supplier["unit_price"][idx] = energy_trends.loc[year, ("gas", "unit_price")]
                    gas_supplier["emissions_per_unit"][idx] = energy_trends.loc[year, ("gas", "emissions_per_unit")]

                    h2_supplier["unit_price"][idx] = energy_trends.loc[year, ("h2", "unit_price")]
                    h2_supplier["emissions_per_unit"][idx] = energy_trends.loc[year, ("h2", "emissions_per_unit")]

        return data

    @classmethod
    def _load_typical_day(cls, config, _path_root: Path, dims: Dims) -> dict:
        cls._init_typical(config, _path_root)

        series_root = Path(_path_root) / config["paths"]["relpath_series"]
        typical_days = config["scenario_specific"]["typical_days"]
        typical_path = series_root / typical_days

        typical_path.mkdir(parents=True, exist_ok=True)

        if not any(typical_path.glob("*.pkl")):
            log.info("No typical periods found. Generating them now...")
            cls.typical.data_to_periods()
        else:
            log.info("Typical periods already exist at %s. Skipping regeneration.", typical_path)

        series_names = config["series_specific"]["series_names"]

        data = {}
        for series_name in series_names:
            pkl_path = series_root / typical_days / f"{series_name}.pkl"
            with pkl_path.open("rb") as f:
                attr: dict = load(f)
            attr = extend_to_years_index(attr, dims)  # ensure extend_to_years_index handles non-tuple keys
            data[series_name] = attr

        weights_path = typical_path / "weights.json"
        with weights_path.open() as f:
            weights: dict = load(f)

        # Add year index
        weights_new = {}
        for year in arange(1, dims.n_years * dims.year_length + 1, dims.year_length):
            weights_new = {
                **weights_new,
                **{
                    (year, int(key)): value * 8760 / (dims.n_time_steps * dims.step_length)
                    for key, value in weights.items()
                },
            }
        data["weights"] = weights_new

        return data

    @classmethod
    def load_data(cls, config, dims: Dims, _path_root: Path):
        data = {}

        data.update(cls._load_typical_day(config, _path_root, dims))
        data.update(cls._load_energy_supplier_data(config, _path_root, dims))

        strategies = config["scenario_specific"]["transformation_strategies"]
        for strategy in strategies:
            data[strategy] = cls._load_static_ies_data(data, config, _path_root, strategy)

        return data

    @classmethod
    def _load_static_ies_data(cls, data, config, _path_root, transformation_strategy: str) -> dict:
        remove_plr = config["investment_specific"]["remove_plr"]
        remove_storage_binary = config["investment_specific"]["remove_storage_binary"]
        global_units_path = Path(_path_root) / config["paths"]["relpath_components"]
        existing_units = config["scenario_specific"]["existing"]

        for file_name in existing_units:
            path = Path(global_units_path) / "existing" / file_name
            data[file_name] = cls._load_config_file(path)

        scenario_units = config["scenario_specific"].get(transformation_strategy, [])
        for file_name in scenario_units:
            data[file_name] = cls._load_config_file(Path(global_units_path) / transformation_strategy / file_name)

        if remove_plr:
            replace_pfr_plr_bpts_with_linear_correlation(data)
        if remove_storage_binary:
            allow_simultaneous_charging_and_discharging_of_storages(data)

        # former dynamic ies data
        plr_min = 0 if remove_plr else 0.2

        invest_units = config["investment_specific"].get("invest_units", [])

        for unit in invest_units:
            eta_tech = 0.6
            hnlt_net = data["hnlt_network"]
            temp_condensation = hnlt_net["T_hot"]
            # TODO (@MFr, #1): fix that only constant values for investment evaluation can be considered
            temp_evaporation = hnlt_net["T_cold"]
            eta_carnot = temp_condensation / (temp_condensation - temp_evaporation)
            cop = eta_carnot * eta_tech
            data[unit] = cls._load_config_file(Path(global_units_path) / "investment" / unit)
            data[unit]["plr_min"] = plr_min
            data[unit]["eta"] = cop

        return data
