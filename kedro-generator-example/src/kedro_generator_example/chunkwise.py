import pandas as pd

from kedro.io.core import (
    get_filepath_str,
)
from kedro.extras.datasets.pandas import CSVDataSet


class ChunkWiseCSVDataSet(CSVDataSet):
    """``ChunkWiseCSVDataSet`` loads/saves data from/to a CSV file using an underlying
    filesystem. It uses pandas to handle the CSV file.
    """
    _overwrite = True

    def _save(self, data: pd.DataFrame) -> None:
        save_path = get_filepath_str(self._get_save_path(), self._protocol)
        # Save the header for the first batch
        if self._overwrite:
            data.to_csv(save_path, index=False, mode="w")
            self._overwrite = False
        else:
            data.to_csv(save_path, index=False, header=False, mode="a")