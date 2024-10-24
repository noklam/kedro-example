"""Project settings. There is no need to edit this file unless you want to change values
from the Kedro defaults. For further information, including these default values, see
https://docs.kedro.org/en/stable/kedro_project_setup/settings.html."""

# Instantiated project hooks.
from typing import Callable
from new_kedro_project.hooks import SparkHooks  # noqa: E402


# Hooks are executed in a Last-In-First-Out (LIFO) order.

from kedro.framework.hooks import hook_impl
import pandas as pd


class DataValidationHook:
    def __init__(
        self,
        rules: dict[str, Callable],
        check_before=False,
        check_after=True,
    ):
        self.check_before = check_before
        self.check_after = check_after
        self.rules = rules

        if check_before:

            @hook_impl
            def before_node_run(self, node, catalog, inputs):
                self._validate_dataset(node, catalog, inputs)

            self.before_node_run = before_node_run

        if check_after:

            @hook_impl
            def after_node_run(self, node, catalog, outputs):
                self._validate_dataset(node, catalog, outputs)

            self.after_node_run = after_node_run

    def _validate_datasets(self, node, catalog, datasets):
        for name, data in datasets.items():
            metadata_key = "checks"
            dataset = catalog._get_dataset(name)
            # https://docs.kedro.org/en/stable/hooks/common_use_cases.html#use-hooks-to-read-metadata-from-datacatalog
            metadata = getattr(dataset, "metadata", None)
            if (
                metadata is not None
                and metadata_key
                in metadata  # Assume we put these kwargs under a key called "checks" in catalog.yml
            ):
                check_metadata = metadata[metadata_key]
                # For individual dataset, different rules can be applied on column level. In reality you probably need a type schema but we keep this simple as an example
                columns = check_metadata["columns"]  # Assume this exists
                for col in columns:
                    rules = columns[col]["rules"]
                    for rule in rules:
                        print(f"Checking '{name}' against rule {rule}")
                        if isinstance(rule, dict):
                            self.check(self.rules[rule.keys()], **rules.values())
                        elif isinstance(
                            rule, str
                        ):  # if the rule doesn't take argument and is simply a list
                            self.check(self.rules[rule])

    def check(self, data, rule: Callable, **validate_kwargs):
        return rule(data, **validate_kwargs)

    # You can also use other hooks spec like before_dataset_loaded if you need fine grain control

