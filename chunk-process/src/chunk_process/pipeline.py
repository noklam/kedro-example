"""
This is a boilerplate pipeline
generated using Kedro 0.18.6
"""

from kedro.pipeline import Pipeline, node, pipeline

from .nodes import process_chunk, split_data


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=split_data,
                inputs=["example_iris_data", "parameters"],
                outputs="X_train_chunk",
                name="split",
            ),
            node(
                func=process_chunk,
                inputs="X_train_chunk",
                outputs="dummy",
                name="process_chunk",
            ),
        ]
    )
