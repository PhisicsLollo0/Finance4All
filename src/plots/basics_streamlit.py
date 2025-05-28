import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.dates import DateFormatter

import seaborn as sns

import plotly.express as px

from src.utils.basics import compute_geometric_mean

import seaborn as sns

import plotly.express as px

DEFAULT_LAYOUT = {
    "template": "simple_white",
    "width": 1200,
    "height": 800,
    "yaxis_tickformat": ".1%",
    "xaxis_title": "Date",
    "yaxis_title": "Annualized Return (%)",
    "legend_title": "Portfolio",
    "title_font_size": 25,
    "title_font_family": "Arial",
    "legend": dict(font=dict(size=22)),
    "xaxis": dict(
        tickformat="%Y",
        title_font=dict(size=22, color="black", family="Arial"),
        tickfont=dict(size=16, color="black"),
        linecolor="black",
        linewidth=2,
        showgrid=True,
        gridcolor="lightgray",
        gridwidth=1
    ),
    "yaxis": dict(
        title_font=dict(size=22, color="black", family="Arial"),
        tickfont=dict(size=16, color="black"),
        linecolor="black",
        linewidth=2,
        showgrid=True,
        gridcolor="lightgray",
        gridwidth=1
    ),
    "font": dict(color="black")
}


def plot_percentage_returns_streamlit(data, start_date=None, end_date=None):
    """
    Returns a Matplotlib Figure of cumulative percentage returns over time.
    """
    data = data.copy()
    data['Date'] = pd.to_datetime(data['Date'], format="%m/%Y")
    if start_date:
        data = data[data['Date'] >= pd.to_datetime(start_date)]
    if end_date:
        data = data[data['Date'] <= pd.to_datetime(end_date)]
    dates = data['Date']
    data = data.drop(columns=['Date'])
    data_returns = data.div(data.iloc[0]).subtract(1).multiply(100)
    df = pd.concat([dates, data_returns], axis=1)
    df.set_index("Date", inplace=True)

    sns.set(style="whitegrid", context="talk")
    fig, ax = plt.subplots(figsize=(14, 7))
    palette = sns.color_palette("tab10", n_colors=len(df.columns))

    for i, col in enumerate(df.columns):
        ax.plot(df.index, df[col], label=col, linewidth=2, color=palette[i])

    ax.set_xlabel("Date")
    ax.set_ylabel("Return (%)")
    ax.set_title("Cumulative Percentage Returns Over Time", fontsize=16, fontweight='bold')
    ax.legend(loc="upper left", fontsize=24)
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.xaxis.set_major_formatter(DateFormatter('%Y'))
    fig.autofmt_xdate()
    fig.tight_layout()
    return fig

def plot_annualized_returns_streamlit(results, years=None):
    """
    Plots the annualized returns of indices over time interactively using Plotly and Seaborn style.
    
    Parameters:
        results (dict or DataFrame): The results data containing 'Date' and portfolio return columns.
        years (int, optional): Number of years used for rolling window annotation.
        width (int): Width of the plot in pixels.
        height (int): Height of the plot in pixels.
    """
    df = pd.DataFrame(results)
    df["Date"] = pd.to_datetime(df["Date"], format="%m/%Y")
    df.set_index("Date", inplace=True)

    # Seaborn style for consistency
    sns.set(style="whitegrid", context="talk")

    # Melt for Plotly
    df_reset = df.reset_index()
    df_melt = df_reset.melt(id_vars="Date", var_name="Portfolio", value_name="Annualized Return")

    fig = px.line(
        df_melt,
        x="Date",
        y="Annualized Return",
        color="Portfolio",
        title=f"Annualized Returns of {years} years rolling windows",
        labels={"Annualized Return": "Annualized Return (%)"},
        template="simple_white"
    )
    fig.update_layout(
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=0.92,
            xanchor="center",
            x=0.5
        )
    )
    fig.update_traces(mode="lines", line=dict(width=2))
    fig.update_layout(**DEFAULT_LAYOUT)

    return fig



def plot_max_drawdown(results):
    """
    Returns a Matplotlib Figure of the maximum drawdown of the portfolios.
    """
    df = pd.DataFrame(results)
    df["Date"] = pd.to_datetime(df["Date"], format="%m/%Y")
    df.set_index("Date", inplace=True)

    sns.set(style="whitegrid", context="talk")
    fig, ax = plt.subplots(figsize=(14, 7))
    palette = sns.color_palette("tab10", n_colors=len(df.columns))

    for i, col in enumerate(df.columns):
        ax.plot(df.index, -df[col], label=col, linewidth=2, color=palette[i])

    ax.set_xlabel("Date")
    ax.set_ylabel("Max Drawdown (%)")
    ax.set_title(f"Max Drawdown since last max", fontsize=16, fontweight='bold')
    ax.legend(loc="lower left", fontsize=14)
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.xaxis.set_major_formatter(DateFormatter('%Y'))
    fig.autofmt_xdate()
    fig.tight_layout()
    return fig

def plot_returns_histogram_streamlit(results, years=20):
    """
    Returns a Matplotlib Figure of the annualized returns histogram.
    """
    df = pd.DataFrame(results)
    geometric_means = compute_geometric_mean(df)
    portfolio_columns = [col for col in df.columns if col != 'Date']
    q5 = df[portfolio_columns].quantile(0.05)

    sns.set(style="whitegrid", context="talk")
    fig, ax = plt.subplots(figsize=(14, 7))
    palette = sns.color_palette("tab10", n_colors=len(df.columns[1:]))

    for i, col in enumerate(df.columns[1:]):
        ax.hist(df[col], histtype='stepfilled', bins=20, alpha=0.2, color=palette[i], label=col)
        ax.hist(df[col], histtype='step', bins=20, alpha=1, color=palette[i])
        ax.axvline(geometric_means[col], color=palette[i], linestyle='-.', linewidth=2)
        ax.axvline(q5[col], color=palette[i], linestyle='--', linewidth=2)

    ax.set_xlabel("Annualized Return")
    ax.set_ylabel("Frequency")
    ax.set_title(f"Annualized Returns of {years} years rolling windows", fontsize=16, fontweight='bold')
    ax.legend(loc="upper left", fontsize=14)
    ax.grid(True, linestyle='--', alpha=0.6)
    fig.tight_layout()
    return fig