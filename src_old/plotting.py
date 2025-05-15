import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def plot_percentage_returns(data, start_date=None, end_date=None):
    # Convert 'Date' column to datetime
    data['Date'] = pd.to_datetime(data['Date'])

    # Apply filtering based on available limits right at the start
    if start_date:
        data = data[data['Date'] >= pd.to_datetime(start_date)]
    if end_date:
        data = data[data['Date'] <= pd.to_datetime(end_date)]

    # Drop the 'Date' column and calculate returns
    dates = data['Date']
    data = data.drop(columns=['Date'])
    data_returns = data.div(data.iloc[0]).subtract(1)

    # Create DataFrame with percentage returns
    df = pd.DataFrame(pd.concat([dates, data_returns], axis=1))

    # Set Date as index
    df.set_index("Date", inplace=True)

    # Plot
    plt.figure(figsize=(10, 5))
    for col in df.columns:
        plt.plot(df.index, df[col], label=col)

    plt.xlabel("Date")
    plt.ylabel("Return (%)")
    plt.title("Returns")
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)

    plt.show()

def plot_annualized_returns(results):
    """
    Plots the annualized returns of indices over time.
    
    Parameters:
        results (dict or DataFrame): A dictionary or DataFrame containing date-indexed annualized return data.
    """
    df = pd.DataFrame(results)
    
    # Ensure Date column is in datetime format and set it as index
    df["Date"] = pd.to_datetime(df["Date"])
    df.set_index("Date", inplace=True)
    
    # Plot
    plt.figure(figsize=(15, 7))
    for col in df.columns:
        plt.plot(df.index, df[col], label=col)
    
    plt.xlabel("Date")
    plt.ylabel("Annualized Return (%)")
    plt.title("Annualized Returns of Indices Over Time")
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.show()

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def plot_returns_distributions(results, colors = ['C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6',]):
    """
    Plots the annualized returns of indices over time and their histograms.
    
    Parameters:
        results (dict or DataFrame): A dictionary or DataFrame containing date-indexed annualized return data.
        colors (list): A list of colors for each dataset.
    """
    df = pd.DataFrame(results)
    
    # Ensure Date column is in datetime format and set it as index
    df["Date"] = pd.to_datetime(df["Date"])
    df.set_index("Date", inplace=True)
    
    # Histogram plot
    plt.figure(figsize=(15, 7))
    for i, col in enumerate(df.columns):
        plt.hist(df[col], label=col, bins=31, color=colors[i], alpha=0.4)
        plt.hist(df[col], bins=31, color=colors[i], histtype='step', lw=2)
        plt.axvline(np.percentile(df[col].values, 5), color=colors[i], ls='--', lw=2)
        plt.axvline(np.percentile(df[col].values, 50), color=colors[i], ls='-', lw=2)
    
    plt.xlabel("Annualized Return (%)")
    plt.ylabel("Frequency")
    plt.title("Distribution of Annualized Returns")
    plt.legend()
    plt.grid(True)
    plt.show()
