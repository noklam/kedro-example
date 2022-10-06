"""Project pipelines."""
from typing import Dict

from kedro.pipeline import Pipeline, pipeline, node


def dummy():
    print("Pipeline is Running - node")
    return "dummy varaible"

node_1 = node(dummy, outputs="dummy", inputs=None, name="dummy")
pipeline = pipeline([node_1])


def register_pipelines() -> Dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns:
        A mapping from a pipeline name to a ``Pipeline`` object.
    """
    return {"__default__":pipeline,
            "dummy_a": pipeline,
            "dummy_b": pipeline}
