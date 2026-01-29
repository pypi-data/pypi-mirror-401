from unittest import TestCase

import numpy as np
from numpy.testing import assert_array_equal
import pandas as pd

from clinbin import classify_blood_pressure, diagnose_metabolic_syndrome
from clinbin.blood import _score_mets_ncep_atp_iii_2005


class TestBloodPressure(TestCase):
    def test_blood_pressure(self):
        """Test all types of blood pressure combinations."""
        index = [
            "alice",
            "bob",
            "charlie",
            "dan",
            "eve",
            "frank",
            "george",
            "harry",
            "irene",
            "john",
        ]
        systolic = pd.Series(
            [80, 120, np.nan, 50, 50, 150, 130, 140, np.nan, 60.0], index=index
        )
        diastolic = pd.Series(
            [60, 60, 80, 80, 100, 60, 100, 80, np.nan, np.nan], index=index
        )
        true_levels = pd.Categorical(
            [
                "normal",
                "elevated",
                np.nan,
                "elevated",
                "hypertension",
                "hypertension",
                "hypertension",
                "hypertension",
                np.nan,
                np.nan,
            ],
            categories=["normal", "elevated", "hypertension"],
            ordered=True,
        )
        bp_levels = classify_blood_pressure(systolic, diastolic)
        self.assertTrue(bp_levels.equals(pd.Series(true_levels, index=index)))


class TestMetabolicSyndrome(TestCase):
    def test_ncpe_atp_iii_2005_criterion(self):
        """Test the metabolic syndrome diagnosis."""
        # Asian woman that scores 3/5, but only when applying ethnicity specific cut-off
        # point.
        alice = {
            # Elevated circumference.
            "waist": 0.8,
            # Normal level, but use medication.
            "triglycerides": 1.6,
            "use_triglyceride_meds": True,
            # Reduced HDL cholesterol.
            "hdl_cholesterol": 1.2,
            "use_hdlc_meds": np.nan,
            # Normal blood pressure.
            "systolic": 120,
            "diastolic": 80,
            "use_blood_pressure_meds": None,
            # Normal glucose.
            "glucose": 5.5,
            "ethnicity": "asian",
            "sex": "female",
        }
        # Asian man with similar values scores 2/5.
        bob = {
            # Normal circumference.
            "waist": 0.8,
            # Normal level, but use medication.
            "triglycerides": 1.6,
            "use_triglyceride_meds": True,
            # Normal HDL cholesterol.
            "hdl_cholesterol": 1.2,
            "use_hdlc_meds": np.nan,
            # Normal blood pressure.
            "systolic": 120,
            "diastolic": 80,
            "use_blood_pressure_meds": None,
            # Normal glucose.
            "glucose": 5.5,
            "ethnicity": "asian",
            "sex": "male",
        }
        # White woman scoring 4/5.
        charlie = {
            # Elevated circumference.
            "waist": 0.88,
            # Normal level.
            "triglycerides": 1.6,
            "use_triglyceride_meds": np.nan,
            # Reduced HDL cholesterol.
            "hdl_cholesterol": 1.1,
            "use_hdlc_meds": np.nan,
            # Elevated blood pressure.
            "systolic": 132,
            "diastolic": 85,
            "use_blood_pressure_meds": None,
            # Elevated glucose.
            "glucose": 5.65,
            "ethnicity": "white",
            "sex": "female",
        }
        # White man with similar values scoring 2/5.
        dan = {
            # Normal circumference.
            "waist": 0.88,
            # Normal level.
            "triglycerides": 1.6,
            "use_triglyceride_meds": np.nan,
            # Normal HDL cholesterol.
            "hdl_cholesterol": 1.1,
            "use_hdlc_meds": np.nan,
            # Elevated blood pressure.
            "systolic": 132,
            "diastolic": 84,
            "use_blood_pressure_meds": None,
            # Elevated glucose.
            "glucose": 5.65,
            "ethnicity": "white",
            "sex": "male",
        }
        # Eve does not have all the information to compute all criteria, but has enough
        # to score 4/5.
        eve = {
            # Elevated circumference.
            "waist": 0.88,
            # Missing triglyceride level.
            "triglycerides": np.nan,
            "use_triglyceride_meds": np.nan,
            # Elevated HDL cholesterol.
            "hdl_cholesterol": 1.1,
            "use_hdlc_meds": np.nan,
            # Elevated blood pressure.
            "systolic": 122,
            "diastolic": 85,
            "use_blood_pressure_meds": None,
            # Elevated glucose.
            "glucose": 5.65,
            "ethnicity": "asian",
            "sex": "female",
        }
        # Frank also doesn't have all the information to compute all criteria. We only
        # know that he meets 1≥ criterion. But we don't know enough to meet the 3/5
        # threshold. Thus, we don't know if Frank is positive, so the score is NaN.
        frank = {
            # Normal circumference.
            "waist": 0.88,
            # Missing triglyceride level.
            "triglycerides": np.nan,
            "use_triglyceride_meds": np.nan,
            # Normal HDL cholesterol.
            "hdl_cholesterol": 1.1,
            "use_hdlc_meds": np.nan,
            # Partially missing blood pressure.
            "systolic": np.nan,
            "diastolic": 84,
            "use_blood_pressure_meds": None,
            # Elevated glucose.
            "glucose": 5.65,
            "ethnicity": "asian",
            "sex": "male",
        }
        names = ["alice", "bob", "charlie", "dan", "eve", "frank"]
        data = pd.DataFrame.from_records(
            [alice, bob, charlie, dan, eve, frank], index=names
        )
        score_card = _score_mets_ncep_atp_iii_2005(
            data["waist"],
            data["triglycerides"],
            data["hdl_cholesterol"],
            data["systolic"],
            data["diastolic"],
            data["glucose"],
            data["sex"],
            data["ethnicity"],
            data["use_triglyceride_meds"],
            data["use_hdlc_meds"],
            data["use_blood_pressure_meds"],
        )

        # (1) Waist circumference
        expected_waist_scores = [1, 0, 1, 0, 1, 0]
        assert_array_equal(score_card["waist"], expected_waist_scores)

        # (2) Triglycerides
        expected_trig_scores = [1, 1, 0, 0, np.nan, np.nan]
        assert_array_equal(score_card["triglycerides"], expected_trig_scores)

        # (3) HDL cholesterol
        expected_hdl_scores = [1, 0, 1, 0, 1, 0]
        assert_array_equal(score_card["hdl_cholesterol"], expected_hdl_scores)

        # (4) Blood pressure
        expected_bp_scores = [0, 0, 1, 1, 1, np.nan]
        assert_array_equal(score_card["blood_pressure"], expected_bp_scores)

        # (5) Fasting glucose
        expected_glucose_scores = [0, 0, 1, 1, 1, 1]
        assert_array_equal(score_card["glucose"], expected_glucose_scores)

        # Test diagnosis.
        diagnoses = diagnose_metabolic_syndrome(**data)
        expected_diagnoses = pd.Series(
            [1, 0, 1, 0, 1, pd.NA], index=names, dtype="Int64"
        )
        self.assertTrue(diagnoses.equals(expected_diagnoses))
