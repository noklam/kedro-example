"""
This is a boilerplate pipeline 'exp'
generated using Kedro 0.17.7
"""

from kedro.pipeline import Pipeline, node, pipeline
import random


def exp_tracking():
    metrics = {'metrics': random.randint(1, 100)}
    columns = ['a', 'b', 'c']

    return metrics, columns


node1 = node(exp_tracking, None, ["metrics", "companies_columns"])


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([node1])
