"""Project pipelines."""
from typing import Dict

from kedro.framework.project import find_pipelines
from kedro.pipeline import Pipeline, node
from kedro.pipeline.modular_pipeline import pipeline
import random


def dummy_func():
    result = random.choice([True, False])
    print("Result: ", result)
    return result


def print_true():
    print("It's TRUE!")
    return "dummy"


def print_false():
    print("It's FALSE!")
    return "dummy"


base_pipeline = pipeline([node(dummy_func, None, "some_condition")])

# Note there are no pipeline that adds all base+true+false pipeline, because they are triggered separately.
true_pipeline = pipeline([node(print_true, None, "dummy")]) # ofcourse you can take some inputs in reality

false_pipeline = pipeline([node(print_false, None, "dummy")])


def register_pipelines() -> Dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns:
        A mapping from pipeline names to ``Pipeline`` objects.
    """
    pipelines = find_pipelines()
    pipelines["__default__"] = base_pipeline
    pipelines["true"] = true_pipeline
    pipelines["false"] = false_pipeline
    return pipelines
