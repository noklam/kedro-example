"""Project settings. There is no need to edit this file unless you want to change values
from the Kedro defaults. For further information, including these default values, see
https://kedro.readthedocs.io/en/stable/kedro_project_setup/settings.html."""

import itertools

from kedro.framework.hooks import hook_impl
from .dagascii import draw


class AsciiHook:
    def _get_pipeline_graph(self, pipeline):
        edges = []

        for node in pipeline.nodes:
            name = f"{node.short_name}"
            for input_ in node.inputs:
                edges.append((input_, name))
            for output_ in node.outputs:
                edges.append((name, output_))
        return edges

    def draw_graph(self, edges, vertexes=None, reverse=True):
        if vertexes is None:
            vertexes = set(itertools.chain(*edges))  # find unique nodes
        if reverse:
            print(edges)
            edges = [(e[1], e[0]) for e in edges]  # Reverse the drawing direction

        print(draw(vertexes, edges))

    def draw_pipeline(self, pipeline):
        graph = self._get_pipeline_graph(pipeline)
        self.draw_graph(graph)

    @hook_impl
    def before_pipeline_run(self, pipeline):
        self.draw_pipeline(pipeline)

    @hook_impl
    def after_catalog_created(self, conf_catalog):
        print(conf_catalog)

# Instantiated project hooks.
# HOOKS = (AsciiHook(),)

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
# from kedro.config import TemplatedConfigLoader
# CONFIG_LOADER_CLASS = TemplatedConfigLoader
# Keyword arguments to pass to the `CONFIG_LOADER_CLASS` constructor.
# CONFIG_LOADER_ARGS = {
#     "globals_pattern": "*globals.yml",
# }

# Class that manages the Data Catalog.
# from kedro.io import DataCatalog
# DATA_CATALOG_CLASS = DataCatalog
