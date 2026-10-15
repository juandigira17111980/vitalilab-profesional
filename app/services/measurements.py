"""Descriptive growth reference, not diagnosis or an exercise prescription."""

import csv
import math
from datetime import date
from functools import lru_cache
from pathlib import Path

from app.extensions import db
from app.models import HealthMeasurement
from app.services.clock import local_day


def age_in_months(birth: date | None, measured_on: date) -> int | None:
    if not birth or birth > measured_on:
        return None
    return (
        (measured_on.year - birth.year) * 12
        + measured_on.month
        - birth.month
        - (measured_on.day < birth.day)
    )


@lru_cache(maxsize=1)
def growth_reference():
    with (Path(__file__).resolve().parents[1] / "data" / "who_bmi_2007.csv").open(
        encoding="utf-8", newline=""
    ) as source:
        return {
            (row["sex"], int(row["month"])): tuple(float(row[key]) for key in ("L", "M", "S"))
            for row in csv.DictReader(source)
        }


def growth_snapshot(bmi: float, birth: date | None, sex: str, measured_on: date) -> dict:
    age = age_in_months(birth, measured_on)
    result = {
        "age_months": age,
        "reference_sex": sex if sex in {"male", "female"} else None,
        "reference_source": None,
        "growth_percentile": None,
    }
    if age is None or not 61 <= age <= 228 or sex not in {"male", "female"}:
        return result
    l_value, median, spread = growth_reference()[(sex, age)]
    z_value = (
        (((bmi / median) ** l_value - 1) / (l_value * spread))
        if l_value
        else math.log(bmi / median) / spread
    )
    result["reference_source"] = "WHO-2007-LMS"
    # Do not extrapolate the normal LMS percentile outside the documented central range.
    if math.isfinite(z_value) and -3 <= z_value <= 3:
        result["growth_percentile"] = round(100 * (1 + math.erf(z_value / math.sqrt(2))) / 2, 2)
    return result


def reference_note(measurement) -> str:
    if measurement.growth_percentile is not None:
        return (
            f"Percentil de referencia OMS: {measurement.growth_percentile:.0f}. "
            "No es una calificación ni un diagnóstico."
        )
    if measurement.age_months is None:
        return (
            "Sin interpretación por edad: completa los datos "
            "solo si deseas una referencia de crecimiento."
        )
    if measurement.age_months < 240:
        return (
            "No se aplican rangos adultos. La edad, el desarrollo "
            "y el contexto requieren valoración profesional."
        )
    return (
        "Una referencia descriptiva; no determina tu salud, tu capacidad "
        "ni la rutina que puedes realizar."
    )


def measurement_history(user, year: int):
    rows = list(
        db.session.scalars(
            db.select(HealthMeasurement)
            .where(
                HealthMeasurement.user_id == user.id,
                HealthMeasurement.measured_on >= date(year, 1, 1),
                HealthMeasurement.measured_on < date(year + 1, 1, 1),
            )
            .order_by(HealthMeasurement.measured_on, HealthMeasurement.id)
        )
    )
    # One last measurement per date in the graph; all rows remain available in the table.
    daily = {row.measured_on: row for row in rows}
    series = list(daily.values())
    values = [float(row.bmi_snapshot) for row in series]
    low, high = (min(values) - 1, max(values) + 1) if values else (0, 1)
    total = (date(year + 1, 1, 1) - date(year, 1, 1)).days - 1
    points = [
        {
            "x": round(35 + 730 * (row.measured_on - date(year, 1, 1)).days / total, 2),
            "y": round(200 - 160 * (float(row.bmi_snapshot) - low) / (high - low), 2),
            "row": row,
        }
        for row in series
    ]
    return {
        "rows": rows,
        "points": points,
        "polyline": " ".join(f"{point['x']},{point['y']}" for point in points),
        "low": round(low, 1),
        "high": round(high, 1),
        "year": year,
        "today": local_day(user),
    }
