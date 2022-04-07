"""Command line tools for manipulating a Kedro project.
Intended to be invoked via `kedro`."""
import os
import shutil
import subprocess
import sys
import webbrowser
from pathlib import Path

import click
from click import secho
from kedro.framework.cli.project import (
    ASYNC_ARG_HELP,
    CONFIG_FILE_HELP,
    FROM_INPUTS_HELP,
    FROM_NODES_HELP,
    LOAD_VERSION_HELP,
    NODE_ARG_HELP,
    PARAMS_ARG_HELP,
    PIPELINE_ARG_HELP,
    RUNNER_ARG_HELP,
    TAG_ARG_HELP,
    TO_NODES_HELP,
    TO_OUTPUTS_HELP,
)
from kedro.framework.cli.utils import (
    CONTEXT_SETTINGS,
    KedroCliError,
    _check_module_importable,
    _config_file_callback,
    _get_values_as_tuple,
    _reformat_load_versions,
    _split_params,
    call,
    command_with_verbosity,
    env_option,
    forward_command,
    python_call,
    split_string,
)
from kedro.framework.session import KedroSession
from kedro.framework.startup import ProjectMetadata
from kedro.utils import load_obj
import pip

EXCLUDE_NODES_HELP = (
    "The opposite of the node_names, you only define the nodes that to be excluded"
)


@click.group(context_settings=CONTEXT_SETTINGS, name=__file__)
def cli():
    """Command line tools for manipulating a Kedro project."""


@cli.command()
@click.option(
    "--from-inputs", type=str, default="", help=FROM_INPUTS_HELP, callback=split_string
)
@click.option(
    "--to-outputs", type=str, default="", help=TO_OUTPUTS_HELP, callback=split_string
)
@click.option(
    "--from-nodes", type=str, default="", help=FROM_NODES_HELP, callback=split_string
)
@click.option(
    "--to-nodes", type=str, default="", help=TO_NODES_HELP, callback=split_string
)
@click.option("--node", "-n", "node_names", type=str, multiple=True, help=NODE_ARG_HELP)
@click.option(
    "--runner", "-r", type=str, default=None, multiple=False, help=RUNNER_ARG_HELP
)
@click.option("--async", "is_async", is_flag=True, multiple=False, help=ASYNC_ARG_HELP)
@env_option
@click.option("--tag", "-t", type=str, multiple=True, help=TAG_ARG_HELP)
@click.option(
    "--load-version",
    "-lv",
    type=str,
    multiple=True,
    help=LOAD_VERSION_HELP,
    callback=_reformat_load_versions,
)
@click.option("--pipeline", "-p", type=str, default=None, help=PIPELINE_ARG_HELP)
@click.option(
    "--config",
    "-c",
    type=click.Path(exists=True, dir_okay=False, resolve_path=True),
    help=CONFIG_FILE_HELP,
    callback=_config_file_callback,
)
@click.option(
    "--params", type=str, default="", help=PARAMS_ARG_HELP, callback=_split_params
)
@click.option(
    "--exclude-nodes", type=str, default="", multiple=True, help=EXCLUDE_NODES_HELP
)
def run(
    tag,
    env,
    runner,
    is_async,
    node_names,
    to_nodes,
    from_nodes,
    from_inputs,
    to_outputs,
    load_version,
    pipeline,
    config,
    params,
    exclude_nodes,
):
    """Run the pipeline."""
    from kedro.framework.project import pipelines

    runner = load_obj(runner or "SequentialRunner", "kedro.runner")
    tag = _get_values_as_tuple(tag) if tag else tag
    node_names = _get_values_as_tuple(node_names) if node_names else node_names
    exclude_nodes = (
        _get_values_as_tuple(exclude_nodes) if exclude_nodes else exclude_nodes
    )
    kedro_pipeline = pipelines[pipeline or "__default__"]
    filtered_pipeline = kedro_pipeline.filter(
        tags=tag,
        from_nodes=from_nodes,
        to_nodes=to_nodes,
        node_names=node_names,
        from_inputs=from_inputs,
        to_outputs=to_outputs,
    )

    # Manually filter out node base on the names
    node_names = set(node.name for node in filtered_pipeline.nodes) - set(exclude_nodes)

    with KedroSession.create(env=env, extra_params=params) as session:
        session.run(
            tags=tag,
            runner=runner(is_async=is_async),
            node_names=node_names,
            from_nodes=from_nodes,
            to_nodes=to_nodes,
            from_inputs=from_inputs,
            to_outputs=to_outputs,
            load_versions=load_version,
            pipeline_name=pipeline,
        )
