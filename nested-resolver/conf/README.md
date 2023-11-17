
# Run
```
kedro run --params key1_="my_num"

>>> {'train_fraction': 0.8, 'random_state': 3, 'target_column': 'species', 'key1': 'foo', 'key1_': 'my_num'}
```

```
>>> {'train_fraction': 0.8, 'random_state': 3, 'target_column': 'species', 'key1': 'foo'}
{'train_fraction': 0.8, 'random_state': 3, 'target_column': 'species', 'key1': 'foo'}
```

# This doesn't work because `params` will override as a dictionary
```
kedro run --params key1_="my_num"
>>> {'train_fraction': 0.8, 'random_state': 3, 'target_column': 'species', 'key1': 'my_num'}
```
