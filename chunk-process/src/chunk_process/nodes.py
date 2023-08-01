"""
This is a boilerplate pipeline
generated using Kedro 0.18.6
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
    # Loop through data in chunks building up the training and test sets
    for i, chunk in enumerate(data):  # Iterate over the chunks from data
        print(f"Process the {i} chunk of data")
        yield chunk


def process_chunk(chunk_data):
    for i, chunk in enumerate(chunk_data):
        print(i, chunk.head())

    return "dummy"