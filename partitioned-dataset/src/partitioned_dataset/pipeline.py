"""
This is a boilerplate pipeline
generated using Kedro 0.18.4
"""

from kedro.pipeline import Pipeline, node, pipeline

from .nodes import dummy


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=dummy,
                inputs="data",
                outputs="1",
            ),
            node(
                func=dummy,
                inputs="data_partitioned",
                outputs="2"
            ),

        ]
    )
