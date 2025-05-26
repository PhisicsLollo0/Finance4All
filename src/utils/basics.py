import pandas as pd
from scipy.stats import gmean


def merge_results(final_results, results):

    if final_results is None:
        return results
    else:
        merged_df = pd.merge(final_results, results, on="Date", how="outer")
        merged_df = merged_df.sort_values(by="Date").reset_index(drop=True)

        # Convert the 'Date' column to datetime (assuming MM/YYYY format)
        merged_df["Date"] = pd.to_datetime(merged_df["Date"], format="%m/%Y")

        # Sort by the datetime values
        merged_df = merged_df.sort_values(by="Date").reset_index(drop=True)

        # (Optional) Convert Date back to MM/YYYY string format if needed
        merged_df["Date"] = merged_df["Date"].dt.strftime("%m/%Y")

        return merged_df
    

def compute_geometric_mean(returns_df):
    """
    Compute geometric mean of returns for each portfolio using scipy.stats.gmean
    """
    portfolio_columns = [col for col in returns_df.columns if col != 'Date']
    
    geo_means = {}
    for col in portfolio_columns:
        clean_returns = returns_df[col].dropna()
        decimal_returns = clean_returns
        geo_mean = gmean(1 + decimal_returns) - 1
        geo_means[col] = geo_mean 
        
    return pd.Series(geo_means).round(4)