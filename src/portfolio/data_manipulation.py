import pandas as pd
from glob import glob
import json

from src.scraping.get_data import *

def select_etfs(data, ETFs):
    sel_columns = ['Date']
    sel_columns.extend(ETFs)
    
    data_pruned = data[sel_columns].dropna(how="all",axis=0).copy()
    data_pruned.dropna(inplace=True)
    return data_pruned

def prune_data_portfolio(portfolio):

    data = get_data_updated_2025()

    ETFs    = list(portfolio.keys())
    weights = list(portfolio.values())

    return select_etfs(data, ETFs), weights

def get_list_of_portfolios():
    
    files = glob('data/portolios/*')
    portfolios = []
    for file in files:
        portfolios.append(file.split('/')[-1].split('.')[0])
    return portfolios

def load_portfolio(portfolio_name):
    """
    Load a portfolio from the data/portfolios directory.
    """
    portfolios = get_list_of_portfolios()
    if portfolio_name not in portfolios:
        raise ValueError(f"Portfolio {portfolio_name} not found. Available portfolios: {portfolios}")
    
    with open(f'data/portolios/{portfolio_name}.json', 'r') as f:
        portfolio = json.load(f)
    
    return portfolio