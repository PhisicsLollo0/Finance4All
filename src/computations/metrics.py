import pandas as pd

from src.portfolio.data_manipulation import *

def max_drawdown(prices):
    """
    Compute the maximum drawdown of a portfolio.
    """
    # Calculate the running maximum
    running_max = None
    maxdrawdown = prices.copy()

    for i in range(len(prices)):
        if running_max is None:
            running_max = prices.iloc[i, 1]
        else:
            running_max = max(running_max, prices.iloc[i, 1])

        maxdrawdown.iloc[i, 1] = (100 * (running_max - prices.iloc[i, 1]) / running_max).round(2)

    return maxdrawdown

def compute_portfolio_prices(portfolio, portfolio_name):
    """
    Compute the prices of a portfolio.
    """
    data, weights = prune_data_portfolio(portfolio)
    dates = data['Date']
    prices = data.iloc[:, 1:].copy() 

    components = prices.columns
    for i in range(len(components)):
        prices[components[i]] = prices[components[i]] * weights[i]/100
    prices = prices.sum(axis=1)
    prices = pd.DataFrame(prices, columns=[portfolio_name])
    prices['Date'] = dates
    prices = prices[['Date', portfolio_name]]

    return prices