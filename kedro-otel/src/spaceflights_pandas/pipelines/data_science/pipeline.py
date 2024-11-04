from blinker import Namespace
from kedro.pipeline import Pipeline, node
from kedro.pipeline.modular_pipeline import pipeline

from .nodes import evaluate_model, split_data, train_model


def create_pipeline(**kwargs) -> Pipeline:
    p= pipeline(
        [
            node(
                func=split_data,
                inputs=["model_input_table", "params:model_options"],
                outputs=["X_train", "X_test", "y_train", "y_test"],
                name="split_data_node",
            ),
            node(
                func=train_model,
                inputs=["X_train", "y_train"],
                outputs="regressor",
                name="train_model_node",
            ),
            node(
                func=evaluate_model,
                inputs=["regressor", "X_test", "y_test"],
                outputs=None,
                name="evaluate_model_node",
            ),

        ],

    )

    nodes =[]
    for n in p.nodes:
        tmp = n
        tmp._namespace="nok"
        nodes.append(tmp)
    p = pipeline(nodes)
    return p
    # i = {}
    # o = {}
    # pa = {}
    # for inp in p.inputs():
    #     print("!!!!", inp)
    #     if isinstance(inp, dict):
    #         pass
    #     elif not inp.startswith("param"):
    #         i[inp] = inp
    #     else:
    #         pa[inp] = inp
    # for out in p.outputs():
    #     o[out] = out
    # p = pipeline(p, namespace="nok",inputs=i, outputs=o, parameters=pa)
    # return p