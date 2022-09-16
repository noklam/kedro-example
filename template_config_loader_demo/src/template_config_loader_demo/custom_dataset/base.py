from typing import Any, Dict

import numpy as np

from kedro.io import AbstractDataSet
from kedro.extras.datasets.pandas import CSVDataSet


class NokDataSet(CSVDataSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)