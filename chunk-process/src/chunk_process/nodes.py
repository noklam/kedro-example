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
    for chunk in data:  # Iterate over the chunks from data
        full_data = pd.concat(
            [chunk]
        )  # Converts the TextFileReader object into list of DataFrames
        data_train = full_data.sample(
            frac=parameters["train_fraction"], random_state=parameters["random_state"]
        )
        data_test = full_data.drop(data_train.index)

        X_train = data_train.drop(columns=parameters["target_column"])
        X_test = data_test.drop(columns=parameters["target_column"])
        y_train = data_train[parameters["target_column"]]
        y_test = data_test[parameters["target_column"]]
        yield X_train


def process_chunk(chunk_data):
    for i, chunk in enumerate(chunk_data):
        print(i, chunk.head())