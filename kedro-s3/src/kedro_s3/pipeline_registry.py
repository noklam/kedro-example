"""Project pipelines."""
from typing import Dict

from kedro.pipeline import Pipeline

from kedro_s3.pipeline import create_pipeline


def register_pipelines() -> Dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns:
        A mapping from a pipeline name to a ``Pipeline`` object.
    """

    return {
        "__default__": create_pipeline(),
    }
