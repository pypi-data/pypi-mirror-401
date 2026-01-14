import itertools

import attrs
import eta_components.milp_component_library as mcl
import numpy as np
import pyomo.environ as pyo


@attrs.define(kw_only=True)
class SystemConfig:
    n_years: int
    n_periods: int
    n_time_steps: int
    step_length: int
    year_length: int
    start_path: str


def extend_to_years_index(data: dict, config: SystemConfig):
    for key, value in data.items():
        if isinstance(value, dict):
            value_temp = {}
            for key2, value2 in value.items():
                for year in np.arange(1, config.n_years * config.year_length + 1, config.year_length):
                    value_temp[(year, *key2)] = value2
            data[key] = value_temp
    return data


def replace_pfr_plr_bpts_with_linear_correlation(data: dict):
    for data_unit in data.values():
        if "pfr_plr_bpts" in data_unit:
            data_unit["pfr_plr_bpts"] = [[0, 0], [1, 1]]


def allow_simultaneous_charging_and_discharging_of_storages(data: dict):
    for name, data_unit in data.items():
        if "storage" in name:
            data_unit["allow_simultaneous_charging_and_discharging"] = True


def aggregate_over_all_indices(var: pyo.Var, system: mcl.custom_types.BasicSystem):
    """
    Aggregiert eine dreifach indizierte Pyomo-Variable
    `var[year, period, time_step]` über alle Indizes
    (Jahr, Periode, Zeitschritt) zu einem einzelnen Skalar.

    Gewichtung:
      - Jeder Beitrag wird mit `weights[year, period]()` multipliziert.
      - Die Gewichte repräsentieren typischerweise die Häufigkeit bzw.
        Dauer einer repräsentativen Periode (z.B. Typtag-Gewichte aus
        Zeitreihenaggregation), sodass eine Skalierung auf Jahresniveau erfolgt.

    Erwartete Struktur:
      - system.sets = (years_set, periods_set, time_set)
      - var ist über genau diese drei Indizes definiert
      - system.objective.weights ist über (year, period) definiert

    Rückgabewert:
      - Skalar, z.B. Gesamtenergie, Gesamtkosten oder Gesamtemissionen
        über alle modellierten Jahre.
    """
    aggregated_value = 0
    weights = system.objective.weights
    for year, period, time_step in itertools.product(*system.sets):
        aggregated_value += var[year, period, time_step]() * weights[year, period]()
    return aggregated_value


def aggregate_over_all_time_steps(var: pyo.Var, year: int, period: int, system: mcl.custom_types.BasicSystem):
    """
    Aggregiert `var[year, period, time_step]` ausschließlich über die
    Zeitschritte einer gegebenen Kombination aus (Jahr, Periode).

    Keine Gewichtung:
      - Es erfolgt keine Multiplikation mit Periodengewichten.
      - Die Funktion liefert die rohe Summe innerhalb einer repräsentativen
        Periode (z.B. Typtag).

    Typische Anwendung:
      - Analyse oder Visualisierung einzelner Perioden
      - Voraggregation, bevor eine gewichtete Jahresskalierung erfolgt

    Rückgabewert:
      - Skalar: Summe über alle Zeitschritte der angegebenen Periode.
    """
    aggregated_value = 0
    for time_step in system.time_set:
        aggregated_value += var[year, period, time_step]()
    return aggregated_value


def aggregate_for_years(var: pyo.Var, system: mcl.custom_types.BasicSystem):
    """
    Aggregiert eine dreifach indizierte Variable `var[year, period, time_step]`
    getrennt für jedes Jahr.

    Gewichtung:
      - Innerhalb jedes Jahres werden alle Perioden und Zeitschritte
        mit `weights[year, period]()` skaliert.
      - Dadurch entsteht ein auf Jahresniveau hochgerechneter Wert
        trotz Verwendung repräsentativer Perioden.

    Typische Anwendung:
      - Berechnung von Jahreskosten, Jahresemissionen oder Jahresenergiemengen
      - Vergleich von Ergebnissen zwischen mehreren Jahren
      - Grundlage für Barwert-, NPV- oder Szenarioanalysen

    Rückgabewert:
      - Dictionary `{year: value}` = a weighted average over the years periods.
      -
    """
    aggregated_list = {}
    weights = system.objective.weights
    for year in system.years_set:
        aggregated_list[year] = 0
        for period in system.periods_set:
            for time_step in system.time_set:
                aggregated_list[year] += (
                    var[year, period, time_step]() * weights[year, period]()
                )  # weights addieren in Summe zu 1
    return aggregated_list
