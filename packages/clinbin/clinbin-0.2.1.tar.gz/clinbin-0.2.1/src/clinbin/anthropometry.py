"""Classify body measurements (anthropometrics) into different levels."""

import pandas as pd

from typing import LiteralString


def _classify_bmi_who2008(x):
    if pd.isna(x):
        return x
    if x < 18.5:
        return "underweight"
    if 18.5 <= x < 25.0:
        return "normal"
    elif 25.0 <= x < 30.0:
        return "overweight"
    elif 30.0 <= x < 35.0:
        return "obesity-CI"
    elif 35.0 <= x < 40.0:
        return "obesity-CII"
    elif x >= 40.0:
        return "obesity-CIII"
    raise ValueError(f"Unknown BMI value x={x}.")


def classify_body_mass_index(
    values: pd.Series, criterion: LiteralString = "who-2008"
) -> pd.Series:
    """Classify body mass index according to World Health Organization cut-off points.

    Classes:
      - `underweight`: <18.5
      - `normal`: 18.5–24.9
      - `overweight`: 25.0–29.9
      - `obesity-CI`: 30.0–34.9
      - `obesity-CII`: 35.0–39.9
      - `obesity-CIII`: ≥40.0

    Args:
        values: Body mass index (kg/m²).
        criterion: Use cut-off points from this organization (`"who-2008"`: Ref. [1]).
    Returns:
        A pandas Series with the corresponding discretized levels.

    References:
        [1] WHO Expert Consultation. Waist circumference and waist-hip ratio. Report of
        a WHO Expert Consultation. Geneva: World Health Organization, 2008:8–11 (2008).
    """
    result: pd.Series = values.map(_classify_bmi_who2008)
    dtype = pd.CategoricalDtype(
        categories=[
            "underweight",
            "normal",
            "overweight",
            "obesity-CI",
            "obesity-CII",
            "obesity-CIII",
        ],
        ordered=True,
    )
    return result.astype(dtype)
