import numpy as np
import pandas as pd

def compute_annualized_return(start_prices, end_prices, weights, years):
    """
    Computes the weighted annualized return over a given number of years.

    Parameters:
    - start_prices (pd.Series): Asset prices at the start of the period.
    - end_prices (pd.Series): Asset prices at the end of the period.
    - weights (np.array): Portfolio weights for the assets.
    - years (int): Number of years in the period.

    Returns:
    - float: Annualized return of the portfolio.
    """
    if len(weights) == 1:  # Handling 100% allocation portfolios
        return (end_prices.iloc[0] / start_prices.iloc[0]) ** (1 / years) - 1
    
    total_return = np.dot(end_prices / start_prices, weights)
    return total_return ** (1 / years) - 1

def get_valid_weights_multi(weight_distribution, asset_list, common_assets):
    """
    Extracts and normalizes the weights of assets present in both time points.

    Parameters:
    - weight_distribution (list): Weights assigned to each asset.
    - asset_list (list): List of all assets.
    - common_assets (list): Assets available in both start and end prices.

    Returns:
    - np.array: Normalized weights.
    """
    selected_weights = [weight_distribution[idx] for idx, asset in enumerate(asset_list) if asset in common_assets]

    if len(selected_weights) == 1:  # If it's a 100% allocation portfolio, no need to normalize
        return np.array(selected_weights)

    return np.array(selected_weights) / sum(selected_weights)

def get_valid_weights(weight_distribution, asset_list, common_assets):
    """
    Extracts and normalizes the weights of assets present in both time points.

    Parameters:
    - weight_distribution (list): Weights assigned to each asset.
    - asset_list (list): List of all assets.
    - common_assets (list): Assets available in both start and end prices.

    Returns:
    - np.array: Normalized weights.
    """
    selected_weights = weight_distribution#[weight_distribution[idx] for idx, asset in enumerate(asset_list) if asset in common_assets]

    if len(selected_weights) == 1:  # If it's a 100% allocation portfolio, no need to normalize
        return np.array(selected_weights)

    return np.array(selected_weights) / sum(selected_weights)

def compute_portfolio_returns(dates, data, asset_list, weights, years=20):
    """
    Computes the weighted annualized return of a portfolio over rolling windows.

    Parameters:
    - data (pd.DataFrame): Asset price data with time indices as rows.
    - asset_list (list): List of all available assets.
    - weight_scenarios (list of lists): Different sets of asset weights to evaluate.
    - years (int, optional): Number of years in each rolling window (default: 20).

    Returns:
    - pd.DataFrame: Annualized returns for different weight distributions.
    """
    
    results = pd.DataFrame()
    num_months = 12 * years
    
    for start_idx in range(len(data.index) - num_months):


        end_idx = start_idx + num_months

        # Extract start and end prices
        start_prices = data.iloc[start_idx]
        end_prices = data.iloc[end_idx]

        # Identify common assets present in both snapshots
        common_assets = start_prices.index.intersection(end_prices.index)

        
        normalized_weights = get_valid_weights(weights, asset_list, common_assets)
            
        if len(normalized_weights) == 0:  # Skip if no valid assets are present
            continue

        annualized_return = compute_annualized_return(start_prices[common_assets], end_prices[common_assets], normalized_weights, years)

            # Store the result
        column_name = ' '.join(map(str, weights))
        results.loc[data.index[start_idx], column_name] = annualized_return

        results_with_data = pd.concat([dates,results], axis=1)

    return results_with_data.dropna()

def compute_portfolio_returns_multi(data, weight_scenarios, years=20):
    """
    Computes the weighted annualized return of a portfolio over rolling windows.

    Parameters:
    - data (pd.DataFrame): Asset price data with time indices as rows.
    - weight_scenarios (list of lists): Different sets of asset weights to evaluate.
    - years (int, optional): Number of years in each rolling window (default: 20).

    Returns:
    - pd.DataFrame: Annualized returns for different weight distributions.
    """
    dates = data['Date']
    asset_list = data.columns[1:].values  # All columns except 'Date'

    results = pd.DataFrame()
    num_months = 12 * years

    for start_idx in range(len(data.index) - num_months):
        end_idx = start_idx + num_months

        # Extract start and end prices (excluding Date column)
        start_prices = data.iloc[start_idx, 1:]  # Drop 'Date' (column 0)
        end_prices = data.iloc[end_idx, 1:]      # Drop 'Date' (column 0)

        # Identify common assets present in both snapshots
        common_assets = start_prices.index.intersection(end_prices.index)

        for weights in weight_scenarios:
            normalized_weights = get_valid_weights_multi(weights, asset_list, common_assets)
            
            if len(normalized_weights) == 0:  # Skip if no valid assets are present
                continue

            # Compute annualized return only for numerical values
            annualized_return = compute_annualized_return(
                start_prices[common_assets], end_prices[common_assets], normalized_weights, years
            )

            # Store the result
            column_name = ' '.join(map(str, weights))
            results.loc[data.index[start_idx], column_name] = annualized_return

    # Concatenate dates and results
    results_with_data = pd.concat([dates, results], axis=1)

    return results_with_data.dropna()

import pandas as pd
import numpy as np

def portfolio_prices(data, weights, TER=0.0):

    TER_perc = TER/100
    """Compute the weighted portfolio price for each date, adjusting for TER (monthly impact)."""
    df = pd.DataFrame(data["Date"].copy())  # Copy date column
    cols = data.columns[1:]  # Select all columns except Date

    if len(weights) != len(cols):
        raise ValueError("Number of weights must match the number of columns (excluding Date).")

    column_name = ' '.join(map(str, weights))  # Create a name for the new column

    # Compute the weighted sum
    df[column_name] = sum(data[col] * w for col, w in zip(cols, weights)) / sum(weights)

    # Convert "Date" to datetime and compute months elapsed
    df["Date"] = pd.to_datetime(df["Date"])  # Ensure Date is in datetime format
    df["Months Elapsed"] = np.arange(len(df))  # Monthly increments (assuming regular time steps)

    # Apply TER as monthly decay
    df[column_name] *= np.exp(-TER_perc / 12 * df["Months Elapsed"])

    return df

def compute_PAC_(df, column_name, contribution=1000, TER=0.0):
    """Simulate a PAC by investing a fixed amount at each time step, considering monthly TER deductions."""
    df = df.copy()  # Avoid modifying the original dataframe

    df["Units"] = contribution / df[column_name]  # Buy units at each time step
    df["Accumulated Units"] = df["Units"].cumsum()  # Cumulative sum of units
    df["Invested Amount"] = contribution * (df.index - df.index[0] + 1)  # Invested amount at each step
    
    # Compute Portfolio Value with TER
    df["Portfolio Value"] = df["Accumulated Units"] * df[column_name]

    return df

def rolling_PAC(data, weights, years=10, contribution=1000, TER=0.0):
    """Compute PAC over rolling windows of a given number of years, considering TER (monthly)."""
    df = portfolio_prices(data, weights, TER=TER)  # Compute weighted portfolio prices
    
    # Set the window size based on the number of years (assuming monthly data)
    window_size = years * 12  

    pac_results = []

    for i in range(len(df) - window_size + 1):
        window_df = df.iloc[i:i + window_size].copy()  # Ensure a copy of the window
        
        # Compute PAC for this window
        window_df = compute_PAC_(window_df, column_name=' '.join(map(str, weights)), contribution=contribution, TER=TER)
        
        # Collect the final result for the rolling window
        result = {
            "Date": window_df.iloc[0]["Date"],  # Starting date of the window
            "Portfolio Value": window_df.iloc[-1]["Portfolio Value"],  # Last value of the Portfolio Value
            "Invested Amount": window_df.iloc[-1]["Invested Amount"]  # Last value of the Invested Amount
        }
        
        pac_results.append(result)

    rolling_pac_df = pd.DataFrame(pac_results)
    rolling_pac_df['Gain'] = rolling_pac_df["Portfolio Value"] / rolling_pac_df["Invested Amount"] - 1
    rolling_pac_df['Annualized Return'] = (rolling_pac_df["Portfolio Value"] / rolling_pac_df["Invested Amount"])**(1/years) - 1

    return rolling_pac_df


def compute_portfolio_returns_combined(data, weight_scenarios, years=20):
    """
    Computes the weighted annualized return of a portfolio over rolling windows for both single and multi-portfolio cases.

    Parameters:
    - data (pd.DataFrame): Asset price data with time indices as rows.
    - weight_scenarios (list or list of lists): A single set of weights or different sets of asset weights to evaluate.
    - years (int, optional): Number of years in each rolling window (default: 20).

    Returns:
    - pd.DataFrame: Annualized returns for the given weight distributions.
    """
    dates = data['Date']
    asset_list = data.columns[1:].values  # All columns except 'Date'

    results = pd.DataFrame()
    num_months = 12 * years

    # Check if weight_scenarios is a list of lists or a single list
    if isinstance(weight_scenarios[0], list):
        # Handle multiple portfolios (list of weight scenarios)
        for start_idx in range(len(data.index) - num_months):
            end_idx = start_idx + num_months

            # Extract start and end prices (excluding Date column)
            start_prices = data.iloc[start_idx, 1:]  # Drop 'Date' (column 0)
            end_prices = data.iloc[end_idx, 1:]      # Drop 'Date' (column 0)

            # Identify common assets present in both snapshots
            common_assets = start_prices.index.intersection(end_prices.index)

            for weights in weight_scenarios:
                normalized_weights = get_valid_weights_multi(weights, asset_list, common_assets)

                if len(normalized_weights) == 0:  # Skip if no valid assets are present
                    continue

                # Compute annualized return only for numerical values
                annualized_return = compute_annualized_return(
                    start_prices[common_assets], end_prices[common_assets], normalized_weights, years
                )

                # Store the result
                column_name = ' '.join(map(str, weights))
                results.loc[data.index[start_idx], column_name] = annualized_return

    else:
        # Handle single portfolio (single set of weights)
        for start_idx in range(len(data.index) - num_months):
            end_idx = start_idx + num_months

            # Extract start and end prices (excluding Date column)
            start_prices = data.iloc[start_idx, 1:]  # Drop 'Date' (column 0)
            end_prices = data.iloc[end_idx, 1:]      # Drop 'Date' (column 0)

            # Identify common assets present in both snapshots
            common_assets = start_prices.index.intersection(end_prices.index)

            normalized_weights = get_valid_weights(weight_scenarios, asset_list, common_assets)

            if len(normalized_weights) == 0:  # Skip if no valid assets are present
                continue

            # Compute annualized return only for numerical values
            annualized_return = compute_annualized_return(
                start_prices[common_assets], end_prices[common_assets], normalized_weights, years
            )

            # Store the result
            column_name = ' '.join(map(str, weight_scenarios))
            results.loc[data.index[start_idx], column_name] = annualized_return

    # Concatenate dates and results
    results_with_data = pd.concat([dates, results], axis=1)

    return results_with_data.dropna()

def compute_PAC(data, weights, contribution=100, TER=0):
    return compute_PAC_(portfolio_prices(data, weights=weights, TER=TER), portfolio_prices(data, weights=weights, TER=TER).columns[1], contribution=contribution, TER=TER)
    #return portfolio_prices(data, weights=weights, TER=TER)
