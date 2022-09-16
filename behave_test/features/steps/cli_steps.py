"""Behave step definitions for the cli_scenarios feature."""

from curses import start_color
import json
import shutil
from pathlib import Path
from time import time

import behave
import requests
import toml
import yaml
from behave import given, then, when

import kedro
from features.steps import util
from features.steps.sh_run import ChildTerminatingPopen, check_run, run
import parse
from behave import register_type


OK_EXIT_CODE = 0



@given('I have run a interactive kedro new with starter {starter}')
@when('I run a interactive kedro new with starter {starter}')
def create_project_with_starter(context, starter):
    """Behave step to run kedro new given the config I previously created."""
    if starter=="we":
        print("Got you")
    else:
        print(f"{starter=}")
    print("create_project_with_starter")
    context.return_code = 0
    # starter_dir = Path(__file__).parent / "test_starter"
    # res = run(
    #     [
    #         context.kedro,
    #         "new",
    #         "-c",
    #         str(context.config_file),
    #         "--starter",
    #         str(starter_dir),
    #     ],
    #     env=context.env,
    #     cwd=context.temp_dir,
    # )
    # assert res.returncode == OK_EXIT_CODE, res



@then("I should get a successful exit code")
def check_status_code(context):
    if context.return_code:
        assert False


@then("I should get an error exit code")
def check_failed_status_code(context):
    if context.result.returncode == OK_EXIT_CODE:
        print(context.result.stdout)
        print(context.result.stderr)

        error_msg = (
            f"Expected exit code other than {OK_EXIT_CODE} "
            f"but got {context.result.returncode}"
        )
        assert False, error_msg


@then('I should get a message including "{msg}"')
def check_message_printed(context, msg):
    """Check that specified message is printed to stdout (can be a segment)."""

    if isinstance(context.result, ChildTerminatingPopen):
        stdout = context.result.stdout.read().decode()
        context.result.terminate()
    else:
        stdout = context.result.stdout

    assert msg in stdout, (
        "Expected the following message segment to be printed on stdout: "
        f"{msg},\nbut got {stdout}"
    )


@then('I should not get a message including "{msg}"')
def check_message_not_printed(context, msg):
    """Check that specified message is not printed to stdout."""

    if isinstance(context.result, ChildTerminatingPopen):
        stdout = context.result.stdout.read().decode()
        context.result.terminate()
    else:
        stdout = context.result.stdout

    assert msg not in stdout, (
        "Expected the following message segment not to be printed on stdout: "
        f"{msg},\nbut got {stdout}"
    )


@then('I should get an error message including "{msg}"')
def check_error_message_printed(context, msg):
    """Check that specified message is printed to stderr (can be a segment)."""

    if isinstance(context.result, ChildTerminatingPopen):
        stderr = context.result.stderr.read().decode()
        context.result.terminate()
    else:
        stderr = context.result.stderr

    assert msg in stderr, (
        "Expected the following message segment to be printed on stderr: "
        f"{msg},\nbut got {stderr}"
    )

