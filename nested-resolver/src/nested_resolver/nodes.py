"""
This is a boilerplate pipeline
generated using Kedro 0.18.13
"""

import logging
from typing import Any, Dict, Tuple

import numpy as np
import pandas as pd


def split_data(
    data: pd.DataFrame, parameters: Dict[str, Any]
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """Splits data into features and target training and test sets.

    Args:
        data: Data containing features and target.
        parameters: Parameters defined in parameters.yml.
    Returns:
        Split data.
    """
    print()
    print(parameters)
    print()


    return "dummy"
