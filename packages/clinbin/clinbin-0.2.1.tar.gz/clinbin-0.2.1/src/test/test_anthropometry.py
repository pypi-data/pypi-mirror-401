from unittest import TestCase

from clinbin import classify_body_mass_index
import numpy as np
import pandas as pd


class TestAnthropometry(TestCase):
    def test_body_mass_index(self):
        """Test the discretization of BMI."""
        bmi = pd.Series([18.49999, 18.5, np.nan, 26, 32, 38.123, 41.0])
        bmi_class = classify_body_mass_index(bmi)
        categories = pd.Categorical(
            [
                "underweight",
                "normal",
                np.nan,
                "overweight",
                "obesity-CI",
                "obesity-CII",
                "obesity-CIII",
            ],
            ordered=True,
            categories=[
                "underweight",
                "normal",
                "overweight",
                "obesity-CI",
                "obesity-CII",
                "obesity-CIII",
            ],
        )
        assert bmi_class.equals(pd.Series(categories, index=bmi.index))
