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
from kedro.extras.datasets.pandas import CSVDataSet

class ChunkWiseCSVDataSet(CSVDataSet):
    """``ChunkWiseCSVDataSet`` loads/saves data from/to a CSV file using an underlying
    filesystem. It uses pandas to handle the CSV file.
    """

    def _save(self, data: pd.DataFrame) -> None:
        save_path = get_filepath_str(self._get_save_path(), self._protocol)

        buf = BytesIO()
        data.to_csv(path_or_buf=buf, **self._save_args)

        with self._fs.open(save_path, mode="ab") as fs_file:
            fs_file.write(buf.getvalue())