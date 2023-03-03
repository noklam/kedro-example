"""partitioned_dataset
"""
from kedro.io.core import AbstractDataSet
from pathlib import Path

__version__ = "0.1"


class CustomDataSet(AbstractDataSet):
    """Minimal Example"""

    def __init__(self, filepath: str):
        self.folder = Path(filepath)

    def _load(self):
        data = []
        for file in self.folder.iterdir():
            with open(file) as f:
                tmp = f.read()
                data.append(tmp)
        return "\n".join(data)

    def _save(self, data) -> None:
        # TODO: finish saving method
        pass

    def _describe(self):
        return "dummy"
