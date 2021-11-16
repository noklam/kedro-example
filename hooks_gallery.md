# Grafana Pipeline Monitor Metrics Hook
```
class PipelineMonitoringHooks:
    def __init__(self):
        self._timers = {}
        self._client = statsd.StatsClient(prefix="kedro")

    @hook_impl
    def before_node_run(self, node: Node) -> None:
        node_timer = self._client.timer(node.name)
        node_timer.start()
        self._timers[node.short_name] = node_timer

    @hook_impl
    def after_node_run(self, node: Node, inputs: Dict[str, Any]) -> None:
        self._timers[node.short_name].stop()
        for dataset_name, dataset_value in inputs.items():
            self._client.gauge(dataset_name + "_size", sys.getsizeof(dataset_value))

    @hook_impl
    def after_pipeline_run(self):
        self._client.incr("run")
```

# DataValidationHook - Great Expectation
```python

class DataValidationHooks:
    def __init__(self) -> None:
        project_root = Path.cwd()
        # ge_contetx_root_dir = project_root / "conf" / "base" / "great_expectations"
        ge_contetx_root_dir = project_root / "great_expectations"
        self._ge_data_context = DataContext(context_root_dir=str(ge_contetx_root_dir))

    # Map expectation to dataset
    DATASET_EXPECTATION_MAPPING = {"TMIS_DATA": "tmis_dataset_expectation"}

    @hook_impl
    def before_node_run(self,node, catalog, inputs) -> None:
        """Validate inputs data to a node based on using great expectation
        if an expectation suite is defined in ``DATASET_EXPECTATION_MAPPING``.
        """
        print("Before Ndoe run")
        self._run_validation(catalog, inputs)

    @hook_impl
    def after_node_run(self, node, catalog, inputs, outputs, is_async, run_id) -> None:
        """Validate outputs data from a node based on using great expectation
        if an expectation suite is defined in ``DATASET_EXPECTATION_MAPPING``.
        """
        print("***********After Node Run:")
        self._run_validation(catalog, outputs)

    def _run_validation(self, catalog: DataCatalog, data: Dict[str, Any], run_id: str=12345):
        for dataset_name, dataset_value in data.items():
            if dataset_name not in self.DATASET_EXPECTATION_MAPPING:
                continue
            print(f"Validating dataset: {dataset_name}")
            dataset = catalog._get_dataset(dataset_name)
            dataset_path = str(dataset._filepath)
            expectation_suite = self.DATASET_EXPECTATION_MAPPING[dataset_name]

            expectation_context = ge.data_context.DataContext()
            batch = expectation_context.get_batch(
                {"path": dataset_path, "datasource": "files_datasource"}, expectation_suite,
            )
            expectation_context.run_validation_operator(
                "action_list_operator", assets_to_validate=[batch], run_id=run_id
            )
```