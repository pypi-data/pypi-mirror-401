"""Classify clinical variables using cut-off points from medical guidelines.

# Installation

```bash
pip3 install git+https://gitlab.com/hylkedonker/clinbin.git
```


"""

from .anthropometry import classify_body_mass_index
from .blood import classify_blood_pressure, diagnose_metabolic_syndrome
from .ehr import classify_chronic_conditions, get_wei2024_multimorbidity_weight_index
