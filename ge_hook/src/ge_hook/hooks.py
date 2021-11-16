# Copyright 2021 QuantumBlack Visual Analytics Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND
# NONINFRINGEMENT. IN NO EVENT WILL THE LICENSOR OR OTHER CONTRIBUTORS
# BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF, OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# The QuantumBlack Visual Analytics Limited ("QuantumBlack") name and logo
# (either separately or in combination, "QuantumBlack Trademarks") are
# trademarks of QuantumBlack. The License does not grant you any right or
# license to the QuantumBlack Trademarks. You may not use the QuantumBlack
# Trademarks or any confusingly similar mark as a trademark for your product,
# or use the QuantumBlack Trademarks in any other manner that might cause
# confusion in the marketplace, including but not limited to in advertising,
# on websites, or on software.
#
# See the License for the specific language governing permissions and
# limitations under the License.

"""Project hooks."""
from pathlib import Path
from typing import Any, Dict, Iterable, Optional

import great_expectations as ge
from great_expectations import DataContext
from kedro.config import ConfigLoader
from kedro.framework.hooks import hook_impl
from kedro.io import DataCatalog
from kedro.versioning import Journal


class ProjectHooks:
    @hook_impl
    def register_config_loader(
        self, conf_paths: Iterable[str], env: str, extra_params: Dict[str, Any]
    ) -> ConfigLoader:
        return ConfigLoader(conf_paths)

    @hook_impl
    def register_catalog(
        self,
        catalog: Optional[Dict[str, Dict[str, Any]]],
        credentials: Dict[str, Dict[str, Any]],
        load_versions: Dict[str, str],
        save_version: str,
        journal: Journal,
    ) -> DataCatalog:
        return DataCatalog.from_config(catalog, credentials, load_versions, save_version, journal)


class DataValidationHooks:
    def __init__(self) -> None:
        project_root = Path.cwd()
        ge_contetx_root_dir = project_root / "conf" / "base" / "great_expectations"
        print(f"***** {ge_contetx_root_dir}")
        # ge_contetx_root_dir = project_root / "great_expectations"
        self._ge_data_context = DataContext(context_root_dir=str(ge_contetx_root_dir))

    # Map expectation to dataset
    DATASET_EXPECTATION_MAPPING = {"example_iris_data": "iris_dataset_expectation"}

    @hook_impl
    def before_node_run(self, node, catalog, inputs) -> None:
        """Validate inputs data to a node based on using great expectation
        if an expectation suite is defined in ``DATASET_EXPECTATION_MAPPING``.
        """
        print("*****Before Ndoe run")
        self._run_validation(catalog, inputs)

    @hook_impl
    def after_node_run(self, node, catalog, inputs, outputs, is_async, run_id) -> None:
        """Validate outputs data from a node based on using great expectation
        if an expectation suite is defined in ``DATASET_EXPECTATION_MAPPING``.
        """
        print("***********After Node Run:")
        self._run_validation(catalog, outputs)

    def _run_validation(self, catalog: DataCatalog, data: Dict[str, Any], run_id: str = 12345):
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

