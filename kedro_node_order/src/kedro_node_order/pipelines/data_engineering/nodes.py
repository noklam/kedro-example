"""Example code for the nodes in the example pipeline. This code is meant
just for illustrating basic Kedro features.

PLEASE DELETE THIS FILE ONCE YOU START WORKING ON YOUR OWN PROJECT!
"""

from typing import Any, Dict

import pandas as pd
import numpy as np
np.random.seed(2022) # Fixed seed
print(np.random.randint(10))
print(np.random.randint(10))

from rich.traceback import install
# install()

def node_1(): # e.g. Model initialization/train/test split
    return '1'

def node_2(x):
    return '2'

def node_3():
    return '3'

def node_4(x):
    raise ValueError
    return '4'

def node_5(x):
    return '5'

def node_iso():
    return '6'