"""Project settings. There is no need to edit this file unless you want to change values
from the Kedro defaults. For further information, including these default values, see
https://docs.kedro.org/en/stable/kedro_project_setup/settings.html."""

# Instantiated project hooks.
# For example, after creating a hooks.py and defining a ProjectHooks class there, do
# from spaceflights_pandas.hooks import ProjectHooks

# Hooks are executed in a Last-In-First-Out (LIFO) order.
import time

from kedro.framework.hooks import hook_impl
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.context import attach, detach, get_current
# Acquire a tracer
tracer = trace.get_tracer("kedro_app.tracer")
# Set up tracing with service name 'kedro_app'
resource = Resource.create({"service.name": "kedro_node_trace"})
trace.set_tracer_provider(TracerProvider(resource=resource))
tracer = trace.get_tracer(__name__)

# Configure OTLP exporter to send traces to the collector
otlp_exporter = OTLPSpanExporter(endpoint="localhost:4317", insecure=True)
trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(otlp_exporter))


class OtelHook:
    @hook_impl
    def before_node_run(self):
      self.node_span = tracer.start_as_current_span("trace")
      self.node_span.__enter__()
      # self.context = attach(self.node_span.get_span_context())
      print("Send something to Otel before node run")
      time.sleep(1)
      print("sleep for 1 sec")

    @hook_impl
    def after_node_run(self):
      with tracer.start_as_current_span("after node run trace") as span:
        print("Send something to Otel after node run")
        #   with tracer.start_as_current_span("trace") as span:
        print("Send something to Otel before node run")
        time.sleep(0.5)
        print("sleep for 0.5 sec")
        # detach(self.context)
      self.node_span.__exit__(None, None, None) # call __exit__ for @contextmanager


HOOKS = (OtelHook(),)

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
from kedro.config import OmegaConfigLoader  # noqa: E402

CONFIG_LOADER_CLASS = OmegaConfigLoader
# Keyword arguments to pass to the `CONFIG_LOADER_CLASS` constructor.
CONFIG_LOADER_ARGS = {
    "base_env": "base",
    "default_run_env": "local",
    #       "config_patterns": {
    #           "spark" : ["spark*/"],
    #           "parameters": ["parameters*", "parameters*/**", "**/parameters*"],
    #       }
}

# Class that manages Kedro's library components.
# from kedro.framework.context import KedroContext
# CONTEXT_CLASS = KedroContext

# Class that manages the Data Catalog.
# from kedro.io import DataCatalog
# DATA_CATALOG_CLASS = DataCatalog
