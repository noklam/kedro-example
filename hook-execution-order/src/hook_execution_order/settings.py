"""Project settings. There is no need to edit this file unless you want to change values
from the Kedro defaults. For further information, including these default values, see
https://docs.kedro.org/en/stable/kedro_project_setup/settings.html."""

# Instantiated project hooks.
# For example, after creating a hooks.py and defining a ProjectHooks class there, do
# from hook_execution_order.hooks import ProjectHooks

# Hooks are executed in a Last-In-First-Out (LIFO) order.
from kedro.framework.hooks import hook_impl
class KedroHook:
    @hook_impl
    def after_node_run(self):
        print("Kedro Hook Function: ", "after_node_run")
    @hook_impl
    def before_node_run(self):
        print("Kedro Hook Function: ", "before_node_run")

    @hook_impl
    def on_node_error(self):
        print("Kedro Hook Function: ", "on_node_error")
    @hook_impl
    def after_context_created(self):
        print("Kedro Hook Function: ", "after_context_created")
    @hook_impl
    def after_pipeline_run(self):
        print("Kedro Hook Function: ", "after_pipeline_run")

    @hook_impl
    def before_pipeline_run(self):
        print("Kedro Hook Function: ", "before_pipeline_run")
    @hook_impl
    def on_pipeline_error(self):
        print("Kedro Hook Function: ", "on_pipeline_error")
    @hook_impl
    def after_dataset_loaded(self):
        print("Kedro Hook Function: ", "after_dataset_loaded")

    @hook_impl
    def after_dataset_saved(self):
        print("Kedro Hook Function: ", "after_dataset_saved")
    @hook_impl
    def before_dataset_loaded(self):
        print("Kedro Hook Function: ", "before_dataset_loaded")
    @hook_impl
    def before_dataset_saved(self):
        print("Kedro Hook Function: ", "before_dataset_saved")

    @hook_impl
    def after_catalog_created(self):
        print("Kedro Hook Function: ", "after_catalog_created")

HOOKS = (KedroHook(),)

# Installed plugins for which to disable hook auto-registration.
# DISABLE_HOOKS_FOR_PLUGINS = ("kedro-viz",)

# Class that manages storing KedroSession data.
# from kedro.framework.session.store import BaseSessionStore
# SESSION_STORE_CLASS = BaseSessionStore
# Keyword arguments to pass to the `SESSION_STORE_CLASS` constructor.
# SESSION_STORE_ARGS = {
#     "path": "./sessions"
# }

# Directory that holds configuration.
# CONF_SOURCE = "conf"

# Class that manages how configuration is loaded.
from kedro.config import OmegaConfigLoader  # noqa: import-outside-toplevel

CONFIG_LOADER_CLASS = OmegaConfigLoader
# Keyword arguments to pass to the `CONFIG_LOADER_CLASS` constructor.
# CONFIG_LOADER_ARGS = {
#       "config_patterns": {
#           "spark" : ["spark*/"],
#           "parameters": ["parameters*", "parameters*/**", "**/parameters*"],
#       }
# }

# Class that manages Kedro's library components.
# from kedro.framework.context import KedroContext
# CONTEXT_CLASS = KedroContext

# Class that manages the Data Catalog.
# from kedro.io import DataCatalog
# DATA_CATALOG_CLASS = DataCatalog
