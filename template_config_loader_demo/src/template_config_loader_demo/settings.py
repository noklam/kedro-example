"""Project settings. There is no need to edit this file unless you want to change values
from the Kedro defaults. For further information, including these default values, see
https://kedro.readthedocs.io/en/stable/kedro_project_setup/settings.html."""

from kedro.framework.hooks import hook_impl

class DebugHook:
    @hook_impl
    def after_catalog_created(catalog, conf_catalog):
        print("Catalog: ")
        print(conf_catalog)



# Instantiated project hooks.
# from template_config_loader_demo.hooks import ProjectHooks
HOOKS = (DebugHook(),)

# Installed plugins for which to disable hook auto-registration.
# DISABLE_HOOKS_FOR_PLUGINS = ("kedro-viz",)

# Class that manages storing KedroSession data.
# from kedro.framework.session.store import ShelveStore
# SESSION_STORE_CLASS = ShelveStore
# Keyword arguments to pass to the `SESSION_STORE_CLASS` constructor.
# SESSION_STORE_ARGS = {
#     "path": "./sessions"
# }

# Class that manages Kedro's library components.
# from kedro.framework.context import KedroContext
# CONTEXT_CLASS = KedroContext

# Directory that holds configuration.
# CONF_SOURCE = "conf"

# Class that manages how configuration is loaded.
from kedro.config import TemplatedConfigLoader

# Easier to understand but requires access to private `_config_mapping`
class MyTemplatedConfigLoader(TemplatedConfigLoader):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.runtime_params:
            self._config_mapping.update(self.runtime_params)

CONFIG_LOADER_CLASS = MyTemplatedConfigLoader # TemplatedConfigLoader
# Keyword arguments to pass to the `CONFIG_LOADER_CLASS` constructor.
CONFIG_LOADER_ARGS = {
    "globals_pattern": "*globals.yml",
}

CONFIG_LOADER_CLASS = MyTemplatedConfigLoader # TemplatedConfigLoader
# Keyword arguments to pass to the `CONFIG_LOADER_CLASS` constructor.
CONFIG_LOADER_ARGS = {
    "globals_pattern": "*globals.yml",
}

# Class that manages the Data Catalog.
# from kedro.io import DataCatalog
# DATA_CATALOG_CLASS = DataCatalog
