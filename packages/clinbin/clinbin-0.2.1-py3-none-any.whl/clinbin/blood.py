"""Classify various measurements pertaining to blood (e.g., pressure)."""

from typing import LiteralString

from numpy import where
import pandas as pd


def _classify_pressure_ehj2024(systolic, diastolic) -> pd.Series:
    blood_pressure_levels = pd.Series(index=systolic.index, dtype=str)
    is_normal = (systolic < 120) & (diastolic < 70)
    blood_pressure_levels[is_normal] = "normal"
    is_elevated = (
        ((systolic >= 120) | (diastolic >= 70)) & (diastolic < 90) & (systolic < 140)
    )
    blood_pressure_levels[is_elevated] = "elevated"
    is_hypertension = (systolic >= 140) | (diastolic >= 90)
    blood_pressure_levels[is_hypertension] = "hypertension"

    # All levels not discretized must be missing.
    is_any = is_normal | is_elevated | is_hypertension
    assert blood_pressure_levels[~is_any].isna().all(), "The levels are non-exhaustive!"
    dtype = pd.CategoricalDtype(
        categories=["normal", "elevated", "hypertension"], ordered=True
    )
    return blood_pressure_levels.astype(dtype)


def classify_blood_pressure(
    systolic: pd.Series, diastolic: pd.Series, criterion: LiteralString = "ESC-2024"
) -> pd.Series:
    """Classify blood pressure according to European Society of Cardiology guidelines.

    Classes:
      - `normal`: <120/70 mmHg
      - `elevated`: 120–139/70–89 mmHg
      - `hypertension`: ≥140/90

    Args:
        systolic: Systolic blood pressure (SBP) in mm Hg.
        diastolic: Diastolic blood pressure (DBP) in mm Hg.
        criterion: Use cut-off points from this guideline (`"ESC-2024"`: Ref. [1])
    Returns:
        A pandas Series with the corresponding discretized levels.

    References:
        [1] McEvoy et al., 2024 ESC Guidelines for the management of elevated blood pressure
        and hypertension  European Heart Journal 45, p. 3936 (2024): ehae178.
    """
    if not all(systolic.index == diastolic.index):
        raise KeyError("The systolic and diastolic indices do not match.")

    return _classify_pressure_ehj2024(systolic, diastolic)


def _has_elevated_waist_circumference(
    waist: pd.Series, sex: pd.Series, ethnicity: pd.Series | None = None
) -> pd.Series:
    """Whether the waist circumference is elevated according to NCEP ATP III 2005.

    Elevated waist circumference:
    Men: ≥1.02 m (≥0.90 m for Asian ancestry),
    Women: ≥0.88 m (≥0.80 m for Asian ancestry).

    Args:
        waist: circumference (m).
    """
    waist_score = pd.Series(index=waist.index)

    # When ethnicity is missing, assume not Asian.
    if ethnicity is None:
        ethnicity = pd.Series("white", index=waist_score.index)
    ethnicity = ethnicity.fillna("white")

    is_asian = ethnicity == "asian"
    is_male = sex == "male"
    is_female = sex == "female"
    big_waist = (
        ~is_asian & ((is_male & (waist >= 1.02)) | (is_female & (waist >= 0.88)))
    ) | (is_asian & ((is_male & (waist >= 0.90)) | (is_female & (waist >= 0.80))))
    waist_score.loc[big_waist] = 1
    normal_waist = (
        ~is_asian & ((is_male & (waist < 1.02)) | (is_female & (waist < 0.88)))
    ) | (is_asian & ((is_male & (waist < 0.90)) | (is_female & (waist < 0.80))))
    waist_score.loc[normal_waist] = 0
    return waist_score


def _has_elevated_triglycerides(
    triglcycerides, use_triglyceride_rx: pd.Series | None = None
):
    """Elevated triglycerides: ≥1.96 mmol/l or triglyceride lowering prescription."""
    trig_score = pd.Series(index=triglcycerides.index)

    # Assume no triglyceride lowering medication usage when the values are absent.
    if use_triglyceride_rx is None:
        use_triglyceride_rx = pd.Series(False, index=trig_score.index)
    use_triglyceride_rx = use_triglyceride_rx.fillna(False)

    trig_score.loc[(triglcycerides >= 1.96) | use_triglyceride_rx] = 1
    trig_score.loc[(triglcycerides < 1.96) & ~use_triglyceride_rx] = 0
    return trig_score


def _has_reduced_hdl_c(
    hdl: pd.Series, sex: pd.Series, use_hdl_rx: pd.Series | None = None
) -> pd.Series:
    """If the HDL cholesterol level are reduced according to NCEP ATP III 2005.

    - HDL prescription
    - Men: <1.0 mmol/l (40 mg/dL)
    - Women: <1.3 mmol/l (50 mg/dL)"""
    hdl_score = pd.Series(index=hdl.index)

    # Assume no HDL cholesterol low medication usage when the values are absent.
    if use_hdl_rx is None:
        use_hdl_rx = pd.Series(False, index=hdl_score.index)
    use_hdl_rx = use_hdl_rx.fillna(False)

    is_male = sex == "male"
    is_female = sex == "female"
    # N.B., Because of missing data, `is_low_hdl` is not the complement of
    # `is_normal_hdl`.
    is_low_hdl = (is_male & (hdl < 1.0)) | (is_female & (hdl < 1.3))
    hdl_score.loc[is_low_hdl | use_hdl_rx] = 1
    is_normal_hdl = (is_male & (hdl >= 1.0)) | (is_female & (hdl >= 1.3))
    hdl_score.loc[is_normal_hdl & ~use_hdl_rx] = 0
    return hdl_score


def _has_elevated_blood_pressure(
    systolic: pd.Series,
    diastolic: pd.Series,
    use_antihypertensive_meds: pd.Series | None = None,
) -> pd.Series:
    """Whether the blood pressure is elevated according to NCEP ATP III 2005.

    Elevated blood pressure:
    - systolic blood pressure ≥130 mm Hg
    - or diastolic blood pressure ≥85 mmHg
    - and/or use of antihypertensive medications.
    """
    bp_score = pd.Series(index=systolic.index)

    # Assume no antihypertensive medication usage when the values are absent.
    if use_antihypertensive_meds is None:
        use_antihypertensive_meds = pd.Series(False, index=bp_score.index)
    use_antihypertensive_meds = use_antihypertensive_meds.fillna(False)

    is_hypertension = (systolic >= 130) | (diastolic >= 85)
    bp_score.loc[is_hypertension | use_antihypertensive_meds] = 1

    is_normotension = (systolic < 130) & (diastolic < 85)
    bp_score.loc[~use_antihypertensive_meds & is_normotension] = 0
    return bp_score


def _has_elevated_fasting_glucose(
    glucose: pd.Series, use_glucose_rx: pd.Series | None = None
):
    """Elevated glucose: ≥5.6 mmol/l (100 mg/dl) or glucose lowering prescription."""
    glucose_score = pd.Series(index=glucose.index)

    # Assume no glucose lowering medication usage when the values are absent.
    if use_glucose_rx is None:
        use_glucose_rx = pd.Series(False, index=glucose_score.index)
    use_glucose_rx = use_glucose_rx.fillna(False)

    glucose_score.loc[(glucose >= 5.6) | use_glucose_rx] = 1
    glucose_score.loc[(glucose < 5.6) & ~use_glucose_rx] = 0
    return glucose_score


def _score_mets_ncep_atp_iii_2005(
    waist: pd.Series,
    triglycerides: pd.Series,
    hdl_cholesterol: pd.Series,
    systolic: pd.Series,
    diastolic: pd.Series,
    glucose: pd.Series,
    sex: pd.Series,
    ethnicity: pd.Series | None = None,
    use_triglyceride_meds: pd.Series | None = None,
    use_hdlc_meds: pd.Series | None = None,
    use_blood_pressure_meds: pd.Series | None = None,
    use_glucose_meds: pd.Series | None = None,
) -> pd.DataFrame:
    """Score the metabolic syndrome according to NCEP ATP III 2005."""
    score_card = {}

    # (1) Waist circumference
    score_card["waist"] = _has_elevated_waist_circumference(waist, sex, ethnicity)
    # (2) Triglycerides
    score_card["triglycerides"] = _has_elevated_triglycerides(
        triglycerides, use_triglyceride_meds
    )
    # (3) HDL cholesterol
    score_card["hdl_cholesterol"] = _has_reduced_hdl_c(
        hdl_cholesterol, sex, use_hdlc_meds
    )
    # (4) Blood pressure
    score_card["blood_pressure"] = _has_elevated_blood_pressure(
        systolic, diastolic, use_blood_pressure_meds
    )
    # (5) Fasting glucose
    score_card["glucose"] = _has_elevated_fasting_glucose(glucose, use_glucose_meds)

    return pd.concat(score_card, axis=1)


def diagnose_metabolic_syndrome(
    waist: pd.Series,
    triglycerides: pd.Series,
    hdl_cholesterol: pd.Series,
    systolic: pd.Series,
    diastolic: pd.Series,
    glucose: pd.Series,
    sex: pd.Series,
    ethnicity: pd.Series | None = None,
    use_triglyceride_meds: pd.Series | None = None,
    use_hdlc_meds: pd.Series | None = None,
    use_blood_pressure_meds: pd.Series | None = None,
    use_glucose_meds: pd.Series | None = None,
    criterion: LiteralString = "NCEP-ATP-III-2005",
) -> pd.Series:
    """Diagnose metabolic syndrome according to clinical guidelines.

    According to NCEP ATP III 2005 (`criterion="NCEP-ATP-III-2005"`), any three of the
    following five criteria:

      - Elevated waist circumference [men: ≥1.02 m (≥0.90 m for Asian ancestry),
          women: ≥0.88 m (≥0.80 m for Asian ancestry)].
      - Elevated triglycerides (≥1.96 mmol/l or triglyceride lowering medication)
      - Reduced HDL cholesterol (men: <1.0 mmol/l, women: <1.3 mmol/l, or HDL-C
          lowering medication).
      - Elevated blood pressure (systolic blood pressure ≥130 mm Hg, or diastolic
          blood pressure ≥85 mm Hg, and/or use of antihypertensive medications).
      - Elevated fasting glucose (≥5.6 mmol/l or glucose lowering medication).

    Args:
        waist: Circumference (m).
        triglycerides: Concentration (mmol/l).
        glucose: fasting glucose in (mmol/l).
        systolic: Systolic blood pressure, SBP (mm Hg).
        diastolic: Diastolic blood pressure, DBP (mm Hg).
        hdl_cholesterol: high-density lipoprotein cholesterol (mmol/l).
        sex: Either `"male"` or `"female"`.
        ethnicity: Use ethnicity specific waist circumferences. Values: `"asian"` or
            anything else.
        use_blood_pressure_meds: A boolean array indicating the use of antihypertensive
            medication. When absent, assume no prescription.
        use_hdlc_meds: A boolean array indicating the use of HDL-C lowering medication.
            When absent, assume no prescription.
        use_glucose_meds: A boolean array indicating the use of glucose lowering
            medication. When absent, assume no prescription.
        use_triglyceride_meds: A boolean array indicating the use of triglyceride
            lowering medication. When absent, assume no prescription.
        criterion: Use cut-off points according to this guideline (`"NCEP-ATP-III-2005"`:
            see Table 2, in Ref. [1]).

    Returns:
        Array indicating whether the patient has metabolic syndrome (1) or not (0).

    References:
        [1] Grundy, Scott M., et al. "Diagnosis and management of the metabolic
        syndrome: an American Heart Association/National Heart, Lung, and Blood
        Institute scientific statement." Circulation 112.17 (2005): 2735-2752.
    """
    score_card = _score_mets_ncep_atp_iii_2005(
        waist,
        triglycerides,
        hdl_cholesterol,
        systolic,
        diastolic,
        glucose,
        sex,
        ethnicity,
        use_triglyceride_meds,
        use_hdlc_meds,
        use_blood_pressure_meds,
        use_glucose_meds,
    )
    # For patients with missing values, we only know they are positive if they score
    # 3 or more.
    diagnoses = pd.Series(index=score_card.index, dtype="Int64")
    is_positive = score_card.sum(axis=1) >= 3
    diagnoses[is_positive] = 1
    is_negative = ~is_positive & score_card.notna().all(axis=1)
    diagnoses[is_negative] = 0
    return diagnoses
