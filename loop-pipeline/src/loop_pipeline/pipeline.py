"""
This is a boilerplate pipeline
generated using Kedro 0.18.6
"""

from kedro.pipeline import Pipeline, node
from kedro.pipeline.modular_pipeline import pipeline

from .nodes import make_monthly_predictions

months = ["jan", "feb", "mar", "apr"]
base_pipeline = pipeline(
    [
        node(
            func=make_monthly_predictions,
            inputs=["input_data"],
            outputs=["output_data"]
        )
    ]
)

def create_pipeline():
    pipelines = []
    for i in range(len(months)):
        if i + 1 >= len(months): break
        curr, next = months[i], months[i+1]
        pipelines.append(pipeline(base_pipeline,
                                  outputs={"output_data":f"{next}.input_data"}, # Override the input definition
                                          namespace=curr))
    return pipeline(pipelines) # Aggregate the pipelines


