# installation
`pip install -e .`~

See notebooks/iceberg-introduction.ipynb for examples

# Example
- Use Iceberg to support incremental workflow

```bash
kedro run --params save_version=2024-11-03,end_date=2024-11-02
kedro run --params save_version=2024-11-03,end_date=2024-11-03
```
# Features supported by Iceberg
- Versioning/branch table


# Problems with Iceberg
- Inefficient use of Iceberg with dataframe. For example, adding a new row in dataframe will be a complete overwrite of existing data. With database (SQL), this can be done as an append operation by parsing SQL statement.
- External Catalog, SQLite limited to single user
- External operation needed, i.e. compacting tables