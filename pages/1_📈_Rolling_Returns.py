import streamlit as st
from src import (
    load_portfolio,
    prune_data_portfolio,
    compute_portfolio_returns_combined,
    merge_results,
    plot_annualized_returns_streamlit,
    plot_returns_histogram_streamlit
)

PORTFOLIOS = [
    '100_2factors',
    '80_20_2factors',
    '80_20_1factor',
    '80_20_ACWI',
    '80_20_World'
]

PORTOFOLIO_NAMES = {
    '100_2factors'  : '100% Stocks + SmallCap Value + Momentum',
    '80_20_2factors': '80% Stocks + 20% Bonds + SmallCap Value + Momentum',
    '80_20_1factor' : '80% Stocks + 20% Bonds + SmallCap Value',
    '80_20_ACWI'    : '80% Stocks(ACWI) + 20% Bonds',
    '80_20_World'   : '80% Stocks(World) + 20% Bonds',
}

def load_and_process_portfolios(portfolio_names, years):
    final_results = None
    for name in portfolio_names:
        portfolio = load_portfolio(name)
        data, weights = prune_data_portfolio(portfolio)
        results = compute_portfolio_returns_combined(data, weights, years=years)
        results = results.rename(columns={results.columns[-1]: name})
        results[name] = results[name].round(5)
        final_results = merge_results(final_results, results) 
        final_results.rename(columns={name: PORTOFOLIO_NAMES[name]}, inplace=True)
    return final_results

def render_tooltip():
    tooltip_html = """
    <style>
    .tooltip {
      position: relative;
      display: inline-block;
      cursor: pointer;
      font-size: 18px;
    }

    .tooltip .tooltiptext {
      visibility: hidden;
      width: 280px;
      background-color: #f0f2f6;
      color: #000;
      text-align: left;
      border-radius: 6px;
      padding: 8px;
      position: absolute;
      z-index: 1;
      top: 50%; 
      left: 125%;
      margin-top: -30px;
      opacity: 0;
      transition: opacity 0.3s;
      box-shadow: 0px 0px 8px rgba(0,0,0,0.1);
    }

    .tooltip:hover .tooltiptext {
      visibility: visible;
      opacity: 1;
    }
    </style>

    <div class="tooltip" style="display:inline-block; vertical-align:middle; cursor:pointer;">
    <svg xmlns="http://www.w3.org/2000/svg" height="20" width="20" fill="#007BFF" viewBox="0 0 16 16">
        <path d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16zm0-1A7 7 0 1 1 8 1a7 7 0 0 1 0 14z"/>
        <path d="m8.93 6.588-2.29.287-.082.38.45.083c.294.07.352.176.288.469l-.738 3.468c-.194.897.105 1.319.808 1.319.545 0 .876-.252 1.02-.598l.088-.416c.066-.292.197-.356.49-.291l.088.02.082-.381-.45-.083c-.294-.07-.35-.176-.288-.47l.738-3.468c.194-.897-.106-1.318-.808-1.318-.545 0-.876.252-1.02.598l-.088.416c-.066.292-.198.356-.49.291z"/>
        <circle cx="8" cy="4.5" r="1"/>
    </svg>
    <span class="tooltiptext">
        This plot shows the annualized returns for each portfolio based on a rolling window.<br>
        Use it to compare long-term trends across strategies.
    </span>
    </div>

    """
    st.markdown(tooltip_html, unsafe_allow_html=True)

def main():

    st.title("Portfolios Rolling Returns Analysis")

    # User input
    col1, col2, col3 = st.columns([8, 2.5, 4.5])
    with col2:
        st.markdown("### Investment Horizon", unsafe_allow_html=True)
        years = st.selectbox(label="Size of the rolling windows",
                                options=[5, 10, 20, 25],
                                index=2, 
                                help="Select the size of the rolling window for annualized returns calculation. Select the number of years similar to the investment horizon you want to analyze.")

    with col1:
        st.markdown("### Select Portfolios")
        if "selected_portfolios" not in st.session_state:
            st.session_state.selected_portfolios = [PORTFOLIOS[0], PORTFOLIOS[1]]

        selected = []
        for p in PORTFOLIOS:
            checked = p in st.session_state.selected_portfolios
            # Make the entire box clickable by using Streamlit's checkbox as the main control
            if st.checkbox(PORTOFOLIO_NAMES[p], value=checked, key=f"portfolio_checkbox_{p}"):
                selected.append(p)

    st.session_state.selected_portfolios = selected
    selected_portfolios = st.session_state.selected_portfolios

    # Data processing
    if not selected_portfolios:
        st.warning("Please select at least one portfolio to analyze.")
        return
    final_results = load_and_process_portfolios(selected_portfolios, years)


    st.markdown("### Annualized Returns")
    cols = st.columns([2, 8])
    with cols[0]:
        with st.expander("ℹ️ What does this mean?"):
            st.markdown("""
            The annualized return is the average return per year over a specified period, adjusted for compounding. It provides a standardized way to compare the performance of different investments over time.
            """)
    fig_annualized = plot_annualized_returns_streamlit(final_results, years=years)
    st.plotly_chart(fig_annualized, use_container_width=True)

    st.subheader(f"Returns Histogram for {years} Years")
    fig_hist = plot_returns_histogram_streamlit(final_results, years=years)
    st.pyplot(fig_hist)

if __name__ == "__main__":
    main()
