import pandas as pd


def select_etfs(data, ETFs):
    sel_columns = ['Date']
    sel_columns.extend(ETFs)
    
    data_pruned = data[sel_columns].dropna(how="all",axis=0).copy()
    data_pruned.dropna(inplace=True)
    return data_pruned