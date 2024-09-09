from kedro.pipeline import Pipeline, node, pipeline

def print_parameters(parameters):
    print(parameters)
    return ["col1", "col2"]

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(print_parameters, "parameters", "updated_params",name="dummy"),
            node(print_parameters, "params:filter_col", "dummy_variable",name="dummy2")
        ]
    )
