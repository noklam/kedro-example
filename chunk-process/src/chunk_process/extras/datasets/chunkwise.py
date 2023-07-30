from copy import deepcopy
from io import BytesIO
from pathlib import PurePosixPath
from typing import Any, Dict

import fsspec
import pandas as pd

from kedro.io.core import (
    AbstractVersionedDataSet,
    Version,
    get_filepath_str,
    get_protocol_and_path,
)


class ChunkWiseCSVDataSet(AbstractVersionedDataSet[pd.DataFrame, pd.DataFrame]):
    """``ChunkWiseCSVDataSet`` loads/saves data from/to a CSV file using an underlying
    filesystem. It uses pandas to handle the CSV file.
    """

    DEFAULT_LOAD_ARGS = {}  # type: Dict[str, Any]
    DEFAULT_SAVE_ARGS = {"index": False}  # type: Dict[str, Any]

    def __init__(
        self,
        filepath: str,
        load_args: Dict[str, Any] = None,
        save_args: Dict[str, Any] = None,
        version: Version = None,
        credentials: Dict[str, Any] = None,
        fs_args: Dict[str, Any] = None,
    ) -> None:
        """Creates a new instance of ``ChunkWiseCSVDataSet`` pointing to a concrete CSV file
        on a specific filesystem.
        """
        _fs_args = deepcopy(fs_args) or {}
        _credentials = deepcopy(credentials) or {}

        protocol, path = get_protocol_and_path(filepath, version)
        if protocol == "file":
            _fs_args.setdefault("auto_mkdir", True)

        self._protocol = protocol
        self._storage_options = {**_credentials, **_fs_args}
        self._fs = fsspec.filesystem(self._protocol, **self._storage_options)

        super().__init__(
            filepath=PurePosixPath(path),
            version=version,
            exists_function=self._fs.exists,
            glob_function=self._fs.glob,
        )

        # Handle default load and save arguments
        self._load_args = deepcopy(self.DEFAULT_LOAD_ARGS)
        if load_args is not None:
            self._load_args.update(load_args)
        self._save_args = deepcopy(self.DEFAULT_SAVE_ARGS)
        if save_args is not None:
            self._save_args.update(save_args)

    def _describe(self) -> Dict[str, Any]:
        return {
            "filepath": self._filepath,
            "protocol": self._load_args,
            "save_args": self._save_args,
            "version": self._version,
        }

    def _load(self) -> pd.DataFrame:
        load_path = str(self._get_load_path())
        return pd.read_csv(load_path, **self._load_args)

    def _save(self, data: pd.DataFrame) -> None:
        save_path = get_filepath_str(self._get_save_path(), self._protocol)

        buf = BytesIO()
        data.to_csv(path_or_buf=buf, **self._save_args)

        with self._fs.open(save_path, mode="a+") as fs_file:
            fs_file.write(buf.getvalue())