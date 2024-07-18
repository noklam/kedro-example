# conditional-kedro-runs

Demonstrate how to do conditional runs outside of Kedro. The key here is to take the result of a kedro run and pipe it into the control flow.

checkout the two files:
- pipeline logic is defined in `pipeline_registry.py` to simplify the case
- `conditional_run.py`


You need to run `python conditional_run.py`.

1. The pipeline generate a random result, i.e. `True` or `False`
2. Conditionally, we will trigger the corresponding pipeline base on the result.