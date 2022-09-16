"""Example code for the nodes in the example pipeline. This code is meant
just for illustrating basic Kedro features.

Delete this when you start working on your own Kedro project.
"""

from kedro.pipeline import node, pipeline

from .nodes import node_1, node_2, node_3, node_4, node_5, node_iso


def multiconcat(*args):
    print(args)
    return "".join(args)

def constant_output():
    return "output"  # pragma: no cover

def create_pipeline(**kwargs):
    return pipeline(
        [
            node(constant_output, None, "A"),
            node(constant_output, None, "B"),
            node(constant_output, None, "C"),
            node(constant_output, None, "D"),
            node(constant_output, None, "E"),
            node(multiconcat, ["A", "B", "C", "D", "E"], "F"),
        ]
    )




    # return pipeline(
    #     [
    #         node(node_1, None, "1"),
    #         node(node_2, "1", "2"),
    #         node(node_1, None, "3"),
    #         node(node_1, None, "4"),
    #         node(node_1, None, "5"),
    #         node(node_1, None, "6")
    #     ]
    # )
