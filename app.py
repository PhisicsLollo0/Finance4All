import streamlit as st

# Import your functions
from src import (
    load_portfolio,
    prune_data_portfolio,
    compute_portfolio_returns_combined,
    merge_results,
    plot_annualized_returns,
    plot_returns_histogram
)

portfolios = [
    '100_2factors',
    '80_20_2factors',
    '80_20_1factor',
    '80_20_ACWI',
    '80_20_World'
]

st.title("Portfolio Returns Visualization")

# User input for years
years = st.selectbox("Select investment horizon (years):", options=[5, 10, 20, 25], index=0)

final_results = None

for portfolio_name in portfolios:
    portfolio = load_portfolio(portfolio_name)
    data, weights = prune_data_portfolio(portfolio)

    results = compute_portfolio_returns_combined(data, weights, years=years)
    results = results.rename(columns={results.columns[-1]: portfolio_name})
    results[portfolio_name] = results[portfolio_name].round(5)

    final_results = merge_results(final_results, results)

st.subheader(f"Annualized Returns for {years} Years")
fig1 = plot_annualized_returns(final_results, years=years)
st.pyplot(fig1)  # or st.plotly_chart if it's a plotly figure

st.subheader(f"Returns Histogram for {years} Years")
fig2 = plot_returns_histogram(final_results, years=years)
st.pyplot(fig2)  # or st.plotly_chart if plotly
