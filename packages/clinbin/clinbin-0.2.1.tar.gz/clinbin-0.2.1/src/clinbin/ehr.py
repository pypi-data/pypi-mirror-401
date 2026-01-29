"""Ways to categorize electronic health record data."""

import json
from pathlib import Path
from typing import LiteralString

import pandas as pd


def _get_definitions_wei2024() -> tuple[
    dict[tuple[str, str], set],
    dict[tuple[str, str], set],
    dict[tuple[str, str], float],
]:
    """Lazy loading of data from JSON.

    Source: Supplementary Table 1 of BMJ open 14.2 (2024): e074390."""
    asset_dir = Path(__file__).parent / "assets"
    with open(asset_dir / "Wei_2024_multimorbidity_weighted_index.json", "r") as f:
        multimorbidity_weighted_index = json.load(f)
    # Make definition as flat dict with sets of ICD-10 codes.
    icd10cm_reference_definitions = {
        (kcond, kcat): payload["ICD-10-CM"]
        for kcond, v in multimorbidity_weighted_index.items()
        for kcat, payload in v.items()
    }

    icd10pcs_reference_definitions = {
        (kcond, kcat): payload["ICD-10-PCS"]
        for kcond, v in multimorbidity_weighted_index.items()
        for kcat, payload in v.items()
    }

    weights = {
        (kcond, kcat): payload["weight"]
        for kcond, v in multimorbidity_weighted_index.items()
        for kcat, payload in v.items()
    }
    return icd10cm_reference_definitions, icd10pcs_reference_definitions, weights


def _is_in_group(target: str, icd10_categories: set[str]) -> bool:
    """Is target ICD10 code contained in or is a child of any code in `icd10_categories`."""
    for reference in icd10_categories:
        # 1. Exact match (e.g., K05 matches K05)
        if target == reference:
            return True

        # 2. Hierarchical match (e.g., K05 matches K05.0)
        # We append a dot to ensure we match the hierarchy boundary
        if target.startswith(reference):
            return True

    return False


def _get_chronic_conditions_matching(
    code: str, reference_definitions: dict[tuple[str, str], set]
) -> list[tuple[str, str]]:
    """Go through all conditions, and see if code matches any of the ICD10 codes."""
    hits = []
    for key, icd10_code_set in reference_definitions.items():
        if _is_in_group(code, icd10_code_set):
            hits.append(key)
    return hits


def classify_chronic_conditions(
    icd10_records: pd.DataFrame, criterion: LiteralString = "wei-2024"
) -> pd.DataFrame:
    r"""Mark the presence of chronic conditions based on diagnoses and procedure codes.

    N.B. The mapping is not isomorphic: one ICD-10 code can cover multiple conditions.

    Args:
        icd10_records: A dataframe with diagnosis codes from the 10th revision of the
            International Classification of Diseases (ICD-10)  (column name:
            `"ICD-10-CM"`) and optionally ICD-10 procedure codes (column name:
            `"ICD-10-PCS"`).
        criterion: Use chronic condition criteria based on this reference
            (`"wei-2024"`: chronic conditions defined in the  multimorbidity-weighted
            index of Wei et al. [1]).

    Returns:
        A dataframe of the same length as `icd10_records`; chronic conditions are marked
        along the columns, where a 0/1 indicates the absence/presence.

    Example:
        ```python
        from clinbin.ehr import classify_chronic_conditions
        import pandas as pd

        records = pd.DataFrame({
            'ICD-10-CM': ['K05.0', 'E08.63', 'E08.631', 'I11.0', 'K04.51', 'I25.7'],
            'ICD-10-PCS': [pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, 'B213'],
        })
        chronic_conds = classify_chronic_conditions(records, criterion="wei-2024")
        ```

    References:
        [1] Wei, Melissa Y., et al. "Development and validation of new
        multimorbidity-weighted index for ICD-10-coded electronic health record
        and claims data: an observational study." BMJ open 14.2 (2024): e074390.
    """
    if "ICD-10-CM" not in icd10_records.columns:
        raise KeyError("No ICD-10-CM column found.")

    if criterion != "wei-2024":
        raise ValueError(
            f"Unknown criterion: {criterion}. Only 'wei-2024' is supported."
        )

    icd10cm_ref_definition, icd10pcs_ref_definition, _ = _get_definitions_wei2024()

    column_names = pd.MultiIndex.from_tuples(
        icd10cm_ref_definition.keys(), names=["condition", "category"]
    )

    output = pd.DataFrame(0, index=icd10_records.index, columns=column_names)

    # Process unique codes instead of codes row-by-row (= faster).
    # Why? The number of unique codes less or equal to the number of rows.
    for code in icd10_records["ICD-10-CM"].dropna().unique():
        # Select all row with this code.
        has_icd10_code = icd10_records["ICD-10-CM"] == code
        matching_conditions = _get_chronic_conditions_matching(
            code, icd10cm_ref_definition
        )
        output.loc[has_icd10_code, matching_conditions] = 1

    if "ICD-10-PCS" in icd10_records.columns:
        for code in icd10_records["ICD-10-PCS"].dropna().unique():
            has_procedure = icd10_records["ICD-10-PCS"] == code
            matching_conditions = _get_chronic_conditions_matching(
                code, icd10pcs_ref_definition
            )
            output.loc[has_procedure, matching_conditions] = 1

    return output.astype("category")


def get_wei2024_multimorbidity_weight_index() -> pd.Series:
    """Get physical functioning of chronic conditions (multimorbidity-weighted index).

    The weights are based on the multimorbidity-weighted index of Wei et al. [1].

    Returns:
        Per chronic condition, the weight of the condition.

    References:
        [1] Wei, Melissa Y., et al. "Development and validation of new
        multimorbidity-weighted index for ICD-10-coded electronic health record
        and claims data: an observational study." BMJ open 14.2 (2024): e074390.
    """
    _, _, weights = _get_definitions_wei2024()
    index = pd.MultiIndex.from_tuples(weights.keys(), names=["condition", "category"])
    return pd.Series(weights, index=index)
