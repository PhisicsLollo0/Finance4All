import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.dates import DateFormatter

def plot_percentage_returns(data, start_date=None, end_date=None):
    # Convert 'Date' column to datetime
    data['Date'] = pd.to_datetime(data['Date'], format="%m/%Y")

    # Apply filtering
    if start_date:
        data = data[data['Date'] >= pd.to_datetime(start_date)]
    if end_date:
        data = data[data['Date'] <= pd.to_datetime(end_date)]

    # Calculate percentage returns
    dates = data['Date']
    data = data.drop(columns=['Date'])
    data_returns = data.div(data.iloc[0]).subtract(1).multiply(100)

    # Combine with dates and set index
    df = pd.concat([dates, data_returns], axis=1)
    df.set_index("Date", inplace=True)

    # Plot setup
    sns.set(style="whitegrid", context="talk")
    plt.figure(figsize=(14, 7))
    palette = sns.color_palette("tab10", n_colors=len(df.columns))

    for i, col in enumerate(df.columns):
        plt.plot(df.index, df[col], label=col, linewidth=2, color=palette[i])

    plt.xlabel("Date")
    plt.ylabel("Return (%)")
    plt.title("Cumulative Percentage Returns Over Time", fontsize=16, fontweight='bold')

    plt.legend(loc="upper left", fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.xticks(rotation=45)

    # Improve date formatting
    ax = plt.gca()
    ax.xaxis.set_major_formatter(DateFormatter('%Y'))

    plt.tight_layout()
    plt.show()

def plot_annualized_returns(results, years=None, plot_figure=True):
    """
    Plots the annualized returns of indices over time.
    
    Parameters:
        results (dict or DataFrame): A dictionary or DataFrame containing date-indexed annualized return data.
    """
    df = pd.DataFrame(results)
    
    # Convert and set date index
    df["Date"] = pd.to_datetime(df["Date"], format="%m/%Y")  # adjust format if needed
    df.set_index("Date", inplace=True)

    # Plot styling
    sns.set(style="whitegrid", context="talk")
    if plot_figure: plt.figure(figsize=(14, 7))
    palette = sns.color_palette("tab10", n_colors=len(df.columns))

    for i, col in enumerate(df.columns):
        plt.plot(df.index, df[col] * 100, label=col, linewidth=2, color=palette[i])

    plt.xlabel("Date")
    plt.ylabel("Annualized Return (%)")
    plt.title(f"Annualized Returns of {years} years rolling windows", fontsize=16, fontweight='bold')

    plt.legend(loc="upper left", fontsize=14)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.xticks(rotation=45)

    # Improve date formatting
    ax = plt.gca()
    ax.xaxis.set_major_formatter(DateFormatter('%Y'))

    plt.tight_layout()

def plot_max_drawdown(results, plot_figure=True):
    """
    Plot the maximum drawdown of the portfolios.
    """

    df = pd.DataFrame(results)
    
    # Convert and set date index
    df["Date"] = pd.to_datetime(df["Date"], format="%m/%Y")  # adjust format if needed
    df.set_index("Date", inplace=True)

    # Plot styling
    sns.set(style="whitegrid", context="talk")
    if plot_figure: plt.figure(figsize=(14, 7))
    palette = sns.color_palette("tab10", n_colors=len(df.columns))

    for i, col in enumerate(df.columns):
        plt.plot(df.index, -df[col], label=col, linewidth=2, color=palette[i])

    plt.xlabel("Date")
    plt.ylabel("Max Drawdown (%)")
    plt.title(f"Max Drawdown since last max", fontsize=16, fontweight='bold')

    plt.legend(loc="lower left", fontsize=14)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.xticks(rotation=45)

    # Improve date formatting
    ax = plt.gca()
    ax.xaxis.set_major_formatter(DateFormatter('%Y'))

    plt.tight_layout()