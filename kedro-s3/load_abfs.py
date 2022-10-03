# from kedro.extras.datasets.pickle import PickleDataSet
import fsspec.registry
from fsspec.registry import known_implementations
known_implementations
path_1 = "abfs://test.pkl"
path_2 = "abfss://test.pkl"
path_3 = "random://test.pkl"

protocol = "abfss"
credentials = {}

fsspec.filesystem(protocol)
# data_1 = PickleDataSet(path_1)
data_2 = PickleDataSet(path_2)
# data_3 = PickleDataSet(path_3)