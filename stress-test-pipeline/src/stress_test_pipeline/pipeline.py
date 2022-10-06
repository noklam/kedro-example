"""
This is a boilerplate pipeline
generated using Kedro 0.18.3
"""
import random
import string
from kedro.pipeline import Pipeline, node, pipeline

from .nodes import make_predictions, report_accuracy, split_data


def generate_node_name(length=6):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = "".join(random.choice(letters) for i in range(length))
    return result_str


def generate_nodes_name(length=10):
    return [generate_node_name() for i in range(length)]


def dummy_func(x):
    return x


def init_func():
    return 1


def generate_nodes(n=10):
    names = generate_nodes_name(n)
    tmp = []
    for i in range(len(names) - 1):
        node_1 = names[i]
        node_2 = names[i + 1]
        if i == 0:
            tmp.append(node(init_func, None, node_1))  # First node without inputs
        tmp.append(node(dummy_func, node_1, node_2))
    return tmp


def create_pipeline():
    return pipeline(generate_nodes(n=10))


# def create_pipeline(**kwargs) -> Pipeline:
#     return pipeline(
#         [
#             node(
#                 func=split_data,
#                 inputs=["example_iris_data", "parameters"],
#                 outputs=["X_train", "X_test", "y_train", "y_test"],
#                 name="split",
#             ),
#             node(
#                 func=make_predictions,
#                 inputs=["X_train", "X_test", "y_train"],
#                 outputs="y_pred",
#                 name="make_predictions",
#             ),
#             node(
#                 func=report_accuracy,
#                 inputs=["y_pred", "y_test"],
#                 outputs=None,
#                 name="report_accuracy",
#             ),
#         ]
#     )
