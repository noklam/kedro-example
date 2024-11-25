from kedro.pipeline import Pipeline, pipeline, node

from .nodes import filter_pypi_data_clickhouse

def create_pipeline(**kwargs):
    return pipeline(
        [
            node(
                func=filter_pypi_data_clickhouse,
                inputs={
                    "table": "clickhouse_pypi_downloads",
                    "start_date": "params:start_date",
                    "end_date": "params:end_date",
                },
                outputs="processed_pypi",
                name="filter_pypi_data_clickhouse",
            )

        ]
    )
