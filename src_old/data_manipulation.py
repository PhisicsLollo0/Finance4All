import pandas as pd
import numpy as np


def prune_data(data, ETFs):
    
    data_pruned = data[np.append(['Date'], ETFs)].dropna(how="all",axis=0).copy()
    data_pruned.dropna(inplace=True)

    return data_pruned['Date'], data_pruned[ETFs]
