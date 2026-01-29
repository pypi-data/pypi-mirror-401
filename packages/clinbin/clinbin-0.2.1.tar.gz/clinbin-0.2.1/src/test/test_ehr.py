from unittest import TestCase

import pandas as pd

from clinbin.ehr import classify_chronic_conditions, _is_in_group


class TestIsInGroup(TestCase):
    def test_icd10_is_in_group(self):
        """Test if hierarchy of ICD10 codes is correctly handled."""
        group = {
            "E08.630",
            "E09.630",
            "E10.630",
            "E11.630",
            "E13.630",
            "K04.5",
            "K05",
            "K08.12",
            "K08.42",
            "C67",
        }

        test_codes = {
            "K05.0": True,  # Child of K05
            "E08.63": False,  # Too coarse
            "E08.631": False,  # Sibling of E08.630 (not a child)
            "K04.5": True,  # Exact Match
            "K04.51": True,  # Child of K04.5
            "Z99": False,  # Unrelated
            "K05": True,  # Exact match
            "K": False,  # Too coarse
            "E08.6": False,  # Too coarse
            "C67.9": True,
        }

        for code, expected in test_codes.items():
            with self.subTest(code=code, expected=expected):
                result = _is_in_group(code, set(group))
                self.assertEqual(result, expected)

    def test_classify_chronic_conditions(self):
        """Test the example in the docstring."""
        records = pd.DataFrame(
            {
                "ICD-10-CM": ["K05.0", "E08.63", "H35.2", "I11.0", "K04.51", "I25.7"],
                "ICD-10-PCS": [pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, "B213"],
            }
        )
        chronic_conds = classify_chronic_conditions(records, criterion="wei-2024")
        # Record 1: child of K05.
        self.assertEqual(chronic_conds.loc[0, ("oral", "Periodontal disease")], 1)
        self.assertEqual(chronic_conds.loc[0].sum(), 1)  # Rest zero
        # Record 2: too coarse to fall within cataract (E08.36), but of diabetes (E08).
        self.assertEqual(chronic_conds.loc[1].sum(), 1)
        # Record 3: sibling of H35.3 (not a child).
        self.assertEqual(chronic_conds.loc[2].sum(), 0)
        # Record 4: I11.0 is in both "Congestive heart failure, Cardiomyopathy"
        # and "High blood pressure, hypertension".
        self.assertEqual(
            chronic_conds.loc[
                3, ("cardiovascular", "High blood pressure, hypertension")
            ],
            1,
        )
        self.assertEqual(
            chronic_conds.loc[
                3, ("cardiovascular", "Congestive heart failure, Cardiomyopathy")
            ],
            1,
        )
        self.assertEqual(chronic_conds.loc[3].sum(), 2)
        # Record 5: Child of K04.5.
        self.assertEqual(chronic_conds.loc[4, ("oral", "Periodontal disease")], 1)
        self.assertEqual(chronic_conds.loc[4].sum(), 1)  # Rest zero
        # Record 6: Has procedure code.
        self.assertEqual(
            chronic_conds.loc[
                5, ("cardiovascular", "Coronary artery bypass graft surgery (CABG)")
            ],
            1,  # B213
        )
        self.assertEqual(chronic_conds.loc[5, ("cardiovascular", "Angina")], 1)  # I25.7
        self.assertEqual(
            chronic_conds.loc[5, ("cardiovascular", "Coronary artery disease")], 1
        )  # I25
        self.assertEqual(chronic_conds.loc[5].sum(), 3)  # Rest zero
