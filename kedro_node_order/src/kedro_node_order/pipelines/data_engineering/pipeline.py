"""Example code for the nodes in the example pipeline. This code is meant
just for illustrating basic Kedro features.

Delete this when you start working on your own Kedro project.
"""

from kedro.pipeline import node, pipeline

from .nodes import node_1, node_2, node_3, node_4, node_5, node_iso


def create_pipeline(**kwargs):
    return pipeline(
        [
            node(node_1, None, "1"),
            node(node_2, "1", "2"),
            node(node_3, None, "3"),
            node(node_4, "3", "4"),
            node(node_5, "4", "5"),
            node(node_iso, None, "6")
        ]
    )
