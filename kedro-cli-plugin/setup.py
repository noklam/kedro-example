from setuptools import find_packages, setup

setup(
    name="kedro-cli-plugin-example",
    version="0.1",
    description="Dummy plugin with hook implementations",
    packages=find_packages(),
    # entry_points={"kedro.project_commands": ["kedrojson = plugin:commands"]},
    entry_points={"kedro.global_commands": ["kedrojson = plugin:commands"]},
)