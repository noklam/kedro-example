from pathlib import Path

import pyarrow as pa
import pyiceberg
from kedro.io.core import AbstractDataset, DatasetError
from pyiceberg.catalog.sql import SqlCatalog
from pyiceberg.table import Table
from typing import Optional

class PyIcebergDataset(AbstractDataset):
    def __init__(
        self,
        table_name,
        namespace="default",
        table_type="pandas",
        load_version=None,
        save_version=None,
        *args,
        **kwargs,
    ):
        self._table: Optional[Table] = None
        self._table_name = table_name
        self._namespace = namespace
        self._save_version = save_version
        self._load_version = load_version
        self.table_type = table_type

        warehouse_path = "tmp/warehouse"
        # TODO: this need to be improved, but enough for demo
        Path(warehouse_path).mkdir(parents=True, exist_ok=True)
        catalog = SqlCatalog(
            namespace,
            **{
                "uri": f"sqlite:///{warehouse_path}/pyiceberg_catalog.db",
                "warehouse": f"file://{warehouse_path}",
            },
        )

        self.catalog = catalog

        # TODO: If table cannot be create, assume it's not created yet and not raise error
        try:
            self._table = self.catalog.load_table(
                f"{self._namespace}.{self._table_name}"
            )
        except:
            pass

    def _save(self, data, version=None):
        arrow_table = pa.Table.from_pandas(data)
        if not self._table:
            # Create the table first
            self.catalog.create_namespace_if_not_exists(self._namespace)
            self._table = self.catalog.create_table(
                f"{self._namespace}.{self._table_name}", schema=arrow_table.schema
            )

        if self.table_type == "pandas":
            self._table.overwrite(arrow_table)
            if self._save_version:
                self._create_version(self._table, self._save_version)
        else:
            raise NotImplementedError

    def _describe(self):
        return {}

    def _check_table_exists(self):
        if not self._table:
            raise DatasetError(
                "Iceberg Table does not exist yet. Use the `save` method to create a table first."
            )

    def _load(self, snapshot_id=None):
        self._check_table_exists()
        if self.table_type == "pandas":
            # TODO
            if snapshot_id:
                pass
            elif self._load_version:
                snapshot_id = self._find_snapshot_id_by_version(self._load_version)
            data = self._table.scan(snapshot_id=snapshot_id).to_pandas()

        return data

    def _create_version(self, table, save_version):
        _ = table.manage_snapshots()
        _.create_tag(
            snapshot_id=self._table.current_snapshot().snapshot_id,
            tag_name=save_version,
        ).commit()

    def _find_snapshot_id_by_version(self, version) -> str:
        snapshot = self._table.snapshot_by_name(version)
        if not snapshot:
            raise ValueError(f"Version `{version}` is not found")
        return snapshot.snapshot_id

    # Shortcut to iceberg table API
    def entries(self):
        return self._table.entries()

    def partitions(self):
        return self._table.partitions()

    def snapshots(self):
        return self._table.snapshots()

    def manifests(self):
        return self._table.manifests()

    def history(self):
        return self._table.history()

    def files(self):
        return self._table.files()

    def schema(self):
        return self._table.schema()

    def latest_version(self):
        return self._table.last_sequence_number
