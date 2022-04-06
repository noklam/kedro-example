from collections import namedtuple
from itertools import cycle
from os.path import join
from pathlib import Path
from unittest.mock import patch

import anyconfig
import click
from click.testing import CliRunner
from pytest import fixture, mark, raises

from kedro import __version__ as version
from kedro.framework.cli import get_project_context, load_entry_points
from kedro.framework.cli.catalog import catalog_cli
from kedro.framework.cli.cli import KedroCLI, _init_plugins, cli
from kedro.framework.cli.jupyter import jupyter_cli
from kedro.framework.cli.micropkg import micropkg_cli
from kedro.framework.cli.pipeline import pipeline_cli
from kedro.framework.cli.project import project_group
from kedro.framework.cli.registry import registry_cli
from kedro.framework.cli.starters import create_cli
from kedro.framework.cli.utils import (
    CommandCollection,
    KedroCliError,
    _clean_pycache,
    _update_value_nested_dict,
    forward_command,
    get_pkg_version,
)
result = CliRunner().invoke(KedroCLI(""), ["new"], input="this will pass")
result = CliRunner().invoke(KedroCLI(""), ["new"], input="this-will-fail")
print(result.output)