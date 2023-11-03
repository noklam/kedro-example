from kedro_datasets.pandas import SQLQueryDataSet

class DummyDataset(SQLQueryDataSet):
    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)

    def _load(self):
        print(self.sql)
        return "dummy"
