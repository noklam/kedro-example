"""
This is a boilerplate pipeline
generated using Kedro 0.18.6
"""

from kedro.pipeline import Pipeline, node
from kedro.pipeline.modular_pipeline import pipeline

from .nodes import make_predictions

# Define a function to generate a pipeline for a given month
def generate_monthly_pipeline(current_month: str, predict_month) -> Pipeline:
    # Define the nodes in the pipeline for this month
    nodes = [
        node(
            func=make_predictions,
            inputs={"input_data": f"my_input_data_{current_month}"},
            outputs={"output_data": f"my_input_data_{predict_month}"}, # output is the input of next node
        )
    ]
    return pipeline(nodes)


# Define the list of months to generate pipelines for
months = ["january", "february", "march"]


def create_pipeline():
    pipelines = []
    for i in range(len(months)):
        if i + 1 < len(months):
            current_month = months[i]
            predict_month = months[i + 1]
            print(f"{current_month=} {predict_month=}")
            pipelines.append(generate_monthly_pipeline(current_month, predict_month))
    return sum(pipelines)

# Or you can use namespace pipeline which append a prefix automatically
