import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.dates import DateFormatter

import seaborn as sns

import plotly.express as px

from src.utils.basics import compute_geometric_mean

import seaborn as sns

import plotly.express as px

import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

DEFAULT_LAYOUT = {
    "template": "simple_white",
    "width": 1200,
    "height": 800,
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
        tickformat=".1f",           # Show one decimal
        tickprefix="",              # No prefix needed; suffix adds %
        ticksuffix="%",            # ✅ Add percent sign without multiplying
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
    """
    df = pd.DataFrame(results)
    df["Date"] = pd.to_datetime(df["Date"], format="%m/%Y")
    df.set_index("Date", inplace=True)

    sns.set(style="whitegrid", context="talk")

    df_reset = df.reset_index()
    df_melt = df_reset.melt(id_vars="Date", var_name="Portfolio", value_name="Annualized Return")

    # Multiply by 100 to convert to percentage
    df_melt["Annualized Return"] *= 100

    fig = px.line(
        df_melt,
        x="Date",
        y="Annualized Return",
        color="Portfolio",
        title=" ",
        template="simple_white"
    )

    fig.update_layout(
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.05,
            xanchor="center",
            x=0.5
        )
    )
    
    # ✨ Custom hover menu
    fig.update_traces(
        mode="lines",
        hovertemplate=(
            "<b>%{fullData.name}</b><br>" +
            "Date: %{x|%b %Y}<br>" +  # Changed to show Month Year
            "Annualized Return: %{y:.2f}%<extra></extra>"
        )
    )

    fig.update_layout(**DEFAULT_LAYOUT)

    return fig

def plot_total_returns_streamlit(results, years=None):
    """
    Plots the total returns of indices over time interactively using Plotly and Seaborn style.

    Parameters:
        results (dict or DataFrame): The results data containing 'Date' and portfolio return columns.
        years (int, optional): Number of years used for rolling window annotation.
    """
    df = pd.DataFrame(results)
    df["Date"] = pd.to_datetime(df["Date"], format="%m/%Y")
    df.set_index("Date", inplace=True)

    sns.set(style="whitegrid", context="talk")

    df_reset = df.reset_index()
    df_melt = df_reset.melt(id_vars="Date", var_name="Portfolio", value_name="Total Return")

    # Multiply by 100 to convert to percentage
    df_melt["Total Return"] *= 100

    fig = px.line(
        df_melt,
        x="Date",
        y="Total Return",
        color="Portfolio",
        title=" ",
        template="simple_white"
    )

    fig.update_layout(
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.05,
            xanchor="center",
            x=0.5
        )
    )
    
    # ✨ Custom hover menu
    fig.update_traces(
        mode="lines",
        hovertemplate=(
            "<b>%{fullData.name}</b><br>" +
            "Date: %{x|%b %Y}<br>" +  # Changed to show Month Year
            "Total Return: %{y:.2f}%<extra></extra>"
        )
    )

    fig.update_layout(**DEFAULT_LAYOUT)

    return fig

def plot_return_distributions_streamlit(df):
    """
    Create an interactive violin plot showing portfolio return distributions,
    with custom median and 5th percentile lines using Plotly and matplotlib colors.
    """
    def _prepare_data(df):
        returns_df = df.dropna(how='all')
        long_df = returns_df.melt(id_vars='Date', var_name='Portfolio', value_name='Return').dropna()
        return long_df

    def _get_colors(portfolios):
        cmap = plt.get_cmap('tab10')
        return {
            p: '#{0:02x}{1:02x}{2:02x}'.format(
                int(255 * r), int(255 * g), int(255 * b)
            )
            for p, (r, g, b, _) in zip(portfolios, cmap(range(len(portfolios))))
        }

    def _get_plot_shapes_and_annotations(medians, p5s, y_positions, colors, line_height=0.6):
        shapes, annotations = [], []
        for portfolio, y_pos in y_positions.items():
            median_val = medians[portfolio]
            p5_val = p5s[portfolio]

            # Median line
            shapes.append(dict(
                type='line', x0=median_val, x1=median_val,
                y0=y_pos - line_height/2, y1=y_pos + line_height/2,
                line=dict(color=colors[portfolio], width=3),
                opacity=1,
                xref='x', yref='y'
            ))
            annotations.append(dict(
                x=median_val, y=y_pos + line_height / 2 + 0.1,
                text=f"Median: {median_val:.2%}",
                showarrow=False,
                font=dict(color=colors[portfolio], size=16),
                xanchor='left'
            ))

            # 5th percentile line
            shapes.append(dict(
                type='line', x0=p5_val, x1=p5_val,
                y0=y_pos - line_height/2, y1=y_pos + line_height/2,
                line=dict(color=colors[portfolio], width=3, dash='dash'),
                opacity=1,
                xref='x', yref='y'
            ))
            annotations.append(dict(
                x=p5_val, y=y_pos - line_height / 2 + 0.65,
                text=f"5th %: {p5_val:.2%}",
                showarrow=False,
                font=dict(color=colors[portfolio], size=16),
                xanchor='left'
            ))

        return shapes, annotations

    # Data preparation
    long_df = _prepare_data(df)
    portfolios = long_df['Portfolio'].unique()
    colors = _get_colors(portfolios)
    plot_height = 230 * len(portfolios)

    # Seaborn style (optional)
    sns.set(style="whitegrid", context="talk")

    # Violin plot
    fig = px.violin(
        long_df,
        y='Portfolio',
        x='Return',
        color='Portfolio',
        box=False,
        points='all',
        color_discrete_map=colors,
        template='simple_white'
    )

    # Order & positioning
    category_order = fig.layout.yaxis.categoryarray or portfolios.tolist()
    y_positions = {p: i for i, p in enumerate(category_order)}

    # Statistics
    medians = long_df.groupby('Portfolio')['Return'].median()
    p5s = long_df.groupby('Portfolio')['Return'].quantile(0.05)
    shapes, annotations = _get_plot_shapes_and_annotations(medians, p5s, y_positions, colors)

    # Final layout update
    fig.update_layout(
        height=plot_height,
        width=1200,
        violingap=0.25,
        violinmode='overlay',
        shapes=shapes,
        annotations=annotations,
        template='simple_white',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.05,
            xanchor="center",
            x=0.5,
            font=dict(size=22)
        ),
        font=dict(color="black"),
        title_font_size=25,
        title_font_family="Arial",
        title = " ",
        xaxis=dict(
            title="Annualized Return (%)",
            title_font=dict(size=22, color="black", family="Arial"),
            tickfont=dict(size=16, color="black"),
            tickformat=".1%",
            linecolor="black",
            linewidth=2,
            showgrid=True,
            gridcolor="lightgray"
        ),
        yaxis=dict(
            title="Portfolio",
            title_font=dict(size=22, color="black", family="Arial"),
            tickfont=dict(size=16, color="black"),
            linecolor="black",
            linewidth=2,
            showgrid=True,
            gridcolor="lightgray",
            categoryorder='array',
            categoryarray=category_order
        )
    )
        # Customize hover template for each trace
    fig.update_traces(
        hoveron = 'points'
        )

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