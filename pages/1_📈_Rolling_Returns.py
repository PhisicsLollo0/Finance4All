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

PORTFOLIO_DESCRIPTIONS = {
    '100_2factors'  : 'This portfolio invests 100% in stocks, focusing on small-cap value and momentum strategies.',
    '80_20_2factors': 'This portfolio allocates 80% to stocks and 20% to bonds, incorporating small-cap value and momentum factors.',
    '80_20_1factor' : 'This portfolio invests 80% in stocks and 20% in bonds, focusing on small-cap value.',
    '80_20_ACWI'    : 'This portfolio invests 80% in global stocks (ACWI) and 20% in bonds.',
    '80_20_World'   : 'This portfolio invests 80% in world stocks and 20% in bonds.'
}

# Add another group of portfolios in col2
SIMPLE_PORTFOLIOS = [
    'lifestrategy100',
    'lifestrategy80',
    'lifestrategy60',
    'lifestrategy40',
    'lifestrategy20',
    'lifestrategy0'
]

SIMPLE_PORTFOLIO_NAMES = {
    'lifestrategy100': '100% Stocks',
    'lifestrategy80' : '80% Stocks + 20% Bonds',
    'lifestrategy60' : '60% Stocks + 40% Bonds',
    'lifestrategy40' : '40% Stocks + 60% Bonds',
    'lifestrategy20' : '20% Stocks + 80% Bonds',
    'lifestrategy0'  : '100% Bonds'
}

SIMPLE_PORTFOLIO_DESCRIPTIONS = {
    'lifestrategy100': 'This portfolio invests 100% in stocks, suitable for aggressive strategies seeking high growth. Note that stocks are MSCI World',
    'lifestrategy80' : 'This portfolio allocates 80% to stocks and 20% to bonds, balancing growth and stability. Stocks are MSCI World',
    'lifestrategy60' : 'This portfolio invests 60% in stocks and 40% in bonds, providing moderate growth with some stability. Stocks are MSCI World',
    'lifestrategy40' : 'This portfolio invests 40% in stocks and 60% in bonds, focusing on stability with some growth potential. Stocks are MSCI World',
    'lifestrategy20' : 'This portfolio invests 20% in stocks and 80% in bonds, prioritizing stability with minimal growth. Stocks are MSCI World',
    'lifestrategy0'  : 'This portfolio invests 100% in bonds, suitable for conservative strategies seeking capital preservation.'
}

ALL_PORTFOLIOS = PORTFOLIOS + SIMPLE_PORTFOLIOS
ALL_PORTFOLIOS_NAMES = {**PORTOFOLIO_NAMES, **SIMPLE_PORTFOLIO_NAMES}
ALL_PORTFOLIOS_DESCRIPTIONS = {**PORTFOLIO_DESCRIPTIONS, **SIMPLE_PORTFOLIO_DESCRIPTIONS}

def load_and_process_portfolios(portfolio_names, years):
    final_results = None
    for name in portfolio_names:
        portfolio = load_portfolio(name)
        data, weights = prune_data_portfolio(portfolio)
        results = compute_portfolio_returns_combined(data, weights, years=years)
        results = results.rename(columns={results.columns[-1]: name})
        results[name] = results[name].round(5)
        final_results = merge_results(final_results, results)
        final_results.rename(columns={name: ALL_PORTFOLIOS_NAMES[name]}, inplace=True)

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
    st.set_page_config(layout="wide")
    st.title("Portfolios Rolling Returns Analysis")

    # User input
    col1, col2, col3, col4 = st.columns([6, 6, 3, 2])
    with col3:
        st.markdown("### Investment Horizon", unsafe_allow_html=True)
        years = st.selectbox(label="Size of the rolling windows",
                                options=[5, 10, 20, 25],
                                index=2, 
                                help="Select the size of the rolling window for annualized returns calculation. Select the number of years similar to the investment horizon you want to analyze.")

    with col1:
        # Put the whole portfolio selection UI in a box
        with st.container(border=True):
            # Header row: "Select Portfolios" and "Select All" toggle side by side
            header_cols = st.columns([7, 3])
            with header_cols[0]:
                st.markdown("### Complex Portfolios")
            with header_cols[1]:
                select_all = st.toggle(
                    "Select All",
                    value=len(st.session_state.get("selected_portfolios", [])) == len(PORTFOLIOS),
                    key="select_all_toggle"
                )

            default_selection = [PORTFOLIOS[0], PORTFOLIOS[1]]

            if "selected_portfolios" not in st.session_state:
                st.session_state.selected_portfolios = default_selection.copy()

            if select_all:
                selected = PORTFOLIOS.copy()
            else:
                # If user just deselected "Select All", reset to default
                if len(st.session_state.get("selected_portfolios", [])) == len(PORTFOLIOS):
                    selected = default_selection.copy()
                else:
                    selected = st.session_state.selected_portfolios.copy()

            for p in PORTFOLIOS:
                checked = p in selected
                cols = st.columns([10, 1])
                with cols[0]:
                    if st.toggle(PORTOFOLIO_NAMES[p], value=checked, key=f"portfolio_toggle_{p}"):
                        if p not in selected:
                            selected.append(p)
                    else:
                        if p in selected:
                            selected.remove(p)
                with cols[1]:
                    # Add an info icon with a tooltip/description
                    st.markdown(
                        f"""
                        <span style="vertical-align:middle;">
                        <span title="{PORTFOLIO_DESCRIPTIONS[p]}">
                            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="#007BFF" viewBox="0 0 16 16" style="margin-left:4px;cursor:pointer;">
                            <path d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16zm0-1A7 7 0 1 1 8 1a7 7 0 0 1 0 14z"/>
                            <path d="m8.93 6.588-2.29.287-.082.38.45.083c.294.07.352.176.288.469l-.738 3.468c-.194.897.105 1.319.808 1.319.545 0 .876-.252 1.02-.598l.088-.416c.066-.292.197-.356.49-.291l.088.02.082-.381-.45-.083c-.294-.07-.35-.176-.288-.47l.738-3.468c.194-.897-.106-1.318-.808-1.318-.545 0-.876.252-1.02.598l-.088.416c-.066.292-.198.356-.49.291z"/>
                            <circle cx="8" cy="4.5" r="1"/>
                            </svg>
                        </span>
                        </span>
                        """,
                        unsafe_allow_html=True
                    )

    with col2:
        with st.container(border=True):
            header_cols = st.columns([7, 3])
            with header_cols[0]:
                st.markdown("### Simple Portfolios")
            with header_cols[1]:
                select_all_simple = st.toggle(
                    "Select All",
                    value=len(st.session_state.get("selected_simple_portfolios", [])) == len(SIMPLE_PORTFOLIOS),
                    key="select_all_simple_toggle"
                )

            default_simple_selection = []#[SIMPLE_PORTFOLIOS[0]]

            if "selected_simple_portfolios" not in st.session_state:
                st.session_state.selected_simple_portfolios = default_simple_selection.copy()

            if select_all_simple:
                selected_simple = SIMPLE_PORTFOLIOS.copy()
            else:
                if len(st.session_state.get("selected_simple_portfolios", [])) == len(SIMPLE_PORTFOLIOS):
                    selected_simple = default_simple_selection.copy()
                else:
                    selected_simple = st.session_state.selected_simple_portfolios.copy()

            for p in SIMPLE_PORTFOLIOS:
                checked = p in selected_simple
                cols = st.columns([10, 1])
                with cols[0]:
                    if st.toggle(SIMPLE_PORTFOLIO_NAMES[p], value=checked, key=f"simple_portfolio_toggle_{p}"):
                        if p not in selected_simple:
                            selected_simple.append(p)
                    else:
                        if p in selected_simple:
                            selected_simple.remove(p)
                with cols[1]:
                    st.markdown(
                        f"""
                        <span style="vertical-align:middle;">
                        <span title="{SIMPLE_PORTFOLIO_DESCRIPTIONS[p]}">
                            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="#007BFF" viewBox="0 0 16 16" style="margin-left:4px;cursor:pointer;">
                            <path d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16zm0-1A7 7 0 1 1 8 1a7 7 0 0 1 0 14z"/>
                            <path d="m8.93 6.588-2.29.287-.082.38.45.083c.294.07.352.176.288.469l-.738 3.468c-.194.897.105 1.319.808 1.319.545 0 .876-.252 1.02-.598l.088-.416c.066-.292.197-.356.49-.291l.088.02.082-.381-.45-.083c-.294-.07-.35-.176-.288-.47l.738-3.468c.194-.897-.106-1.318-.808-1.318-.545 0-.876.252-1.02.598l-.088.416c-.066.292-.198.356-.49.291z"/>
                            <circle cx="8" cy="4.5" r="1"/>
                            </svg>
                        </span>
                        </span>
                        """,
                        unsafe_allow_html=True
                    )

    # Combine selections from both groups
    selected = selected + [p for p in selected_simple if p not in selected]

    st.session_state.selected_portfolios = selected
    selected_portfolios = st.session_state.selected_portfolios

    # Data processing
    if not selected_portfolios:
        st.warning("Please select at least one portfolio to analyze.")
        return

    final_results = load_and_process_portfolios(selected_portfolios, years)


    st.markdown(f"### Annualized Returns for {years} Years Rolling Window")
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
