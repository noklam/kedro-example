"""
This is a boilerplate pipeline
generated using Kedro 0.18.11
"""

import logging
from typing import Any, Dict, Tuple, Iterator
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
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

    data_train = data.sample(
        frac=parameters["train_fraction"], random_state=parameters["random_state"]
    )
    data_test = data.drop(data_train.index)

    X_train = data_train.drop(columns=parameters["target_column"])
    X_test = data_test.drop(columns=parameters["target_column"])
    y_train = data_train[parameters["target_column"]]
    y_test = data_test[parameters["target_column"]]

    label_encoder = LabelEncoder()
    label_encoder.fit(pd.concat([y_train, y_test]))
    y_train = label_encoder.transform(y_train)

    return X_train, X_test, y_train, y_test


def make_predictions(
    X_train: pd.DataFrame, X_test: pd.DataFrame, y_train: pd.Series
) -> pd.Series:
    """Use a DecisionTreeClassifier model to make prediction."""
    model = DecisionTreeClassifier()
    model.fit(X_train, y_train)

    for chunk in X_test:
        y_pred = model.predict(chunk)
        y_pred = pd.DataFrame(y_pred)
        print(y_pred.shape)
        yield y_pred


def report_accuracy(y_pred: pd.Series, y_test: pd.Series):
    """Calculates and logs the accuracy.

    Args:
        y_pred: Predicted target.
        y_test: True target.
    """
    accuracy = accuracy_score(y_test, y_pred)
    logger = logging.getLogger(__name__)
    logger.info("Model has accuracy of %.3f on test data.", accuracy)
