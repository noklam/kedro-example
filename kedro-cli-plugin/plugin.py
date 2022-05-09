import click
from kedro.framework.project import pipelines


@click.group(name="JSON")
def commands():
    """Kedro plugin for printing the pipeline in JSON format"""
    pass


@commands.command()
@click.pass_obj
def to_json(metadata):
    """Display the pipeline in JSON format"""
    pipeline = pipelines["__default__"]
    print(pipeline.to_json())