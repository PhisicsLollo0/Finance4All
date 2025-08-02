import streamlit as st
from pathlib import Path
from src import (
    load_portfolio,
    prune_data_portfolio,
    compute_portfolio_returns_combined,
    merge_results,
    plot_annualized_returns_streamlit,
    plot_total_returns_streamlit,
    plot_return_distributions_streamlit
)

from src.utils.stramlit_basics import deploy_sidebar_menu, deploy_footer

from src.utils.constants import PORTFOLIOS, PORTFOLIO_NAMES, PORTFOLIO_DESCRIPTIONS
from src.utils.constants import SIMPLE_PORTFOLIOS, SIMPLE_PORTFOLIO_NAMES, SIMPLE_PORTFOLIO_DESCRIPTIONS
from src.utils.constants import ALL_PORTFOLIOS, ALL_PORTFOLIOS_NAMES, ALL_PORTFOLIOS_DESCRIPTIONS

# ========================================================================================================
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

    final_results_totalreturn = final_results.copy()
    for name in final_results_totalreturn.keys()[1:]: 
        final_results_totalreturn[name] = (final_results[name] + 1)**years - 1

    return final_results, final_results_totalreturn


# === Setup page ===    
st.set_page_config(
    layout="wide", 
    menu_items=None,)
st.title("Portfolios Rolling Returns Analysis")

# === Sidebar ===    
deploy_sidebar_menu()

# User input
col1, col2, col3, col4 = st.columns([6, 6, 3, 2])
with col3:
    st.markdown("### Investment Horizon", unsafe_allow_html=True)
    years = st.selectbox(label="Size of the rolling windows",
                            options=[5, 10, 15, 20, 25],
                            index=2, 
                            help="Select the size of the rolling window for annualized returns calculation. Select the number of years similar to the investment horizon you want to analyze.")
    st.markdown("### Total or Annualized Returns", unsafe_allow_html=True)
    total_or_annualized = st.toggle(
        "Annualized Returns",
        value=True,
        key="total_or_annualized_toggle",
        help="Select whether to display total returns or annualized returns. Total returns show the overall performance, while annualized returns provide a yearly average performance over the specified period."
    )
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

        default_selection = [PORTFOLIOS[0], PORTFOLIOS[2]]

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
                if st.toggle(PORTFOLIO_NAMES[p], value=checked, key=f"portfolio_toggle_{p}"):
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

final_results, final_results_totalreturn = load_and_process_portfolios(selected_portfolios, years)

if total_or_annualized == True:

    st.markdown(f"### Annualized Returns for {years} Years Rolling Window")
    cols = st.columns([8, 8])
    with cols[0]:
        with st.expander("ℹ️ What does this mean?"):
            st.markdown("""
            The annualized return is the average return per year over a specified period, adjusted for compounding. It provides a standardized way to compare the performance of different investments over time.
            """)

    fig_annualized = plot_annualized_returns_streamlit(final_results, years=years)
    st.plotly_chart(fig_annualized, use_container_width=True)

else:

    st.markdown(f"### Total Returns for {years} Years Rolling Window")
    cols = st.columns([8, 8])
    with cols[0]:
        with st.expander("ℹ️ What does this mean?"):
            st.markdown("""
            sss        """)
    fig_total= plot_total_returns_streamlit(final_results_totalreturn, years=years)
    st.plotly_chart(fig_total, use_container_width=True)


st.divider()

if total_or_annualized == True:

    st.markdown(f"### Distribution of Annualized Returns for {years} Years Rolling Window")
    cols = st.columns([8, 8])
    with cols[0]:
        with st.expander("ℹ️ What does this mean?"):
            st.markdown("""
            The distribution of annualized returns shows how the returns of each portfolio are distributed. It helps identify the range of returns, the average return, and the variability of returns across different portfolios. The plots reports the median return and the 5th percentile return for each portfolio, which can help you understand the risk and potential downside of each strategy.
            The 5th percentile return shows the lower end of the distribution, and practically indicates how the 5% of worst performing scenarios look like for each portfolio.
            """)
    fig_distributions = plot_return_distributions_streamlit(final_results)
    st.plotly_chart(fig_distributions, use_container_width=True)

else:

    st.markdown(f"### Distribution of Total Returns for {years} Years Rolling Window")
    cols = st.columns([8, 8])
    with cols[0]:
        with st.expander("ℹ️ What does this mean?"):
            st.markdown("""
            The distribution of total returns shows how the returns of each portfolio are distributed. It helps identify the range of returns, the average return, and the variability of returns across different portfolios. The plots reports the median return and the 5th percentile return for each portfolio, which can help you understand the risk and potential downside of each strategy.
            The 5th percentile return shows the lower end of the distribution, and practically indicates how the 5% of worst performing scenarios look like for each portfolio.
            """)
    fig_distributions = plot_return_distributions_streamlit(final_results_totalreturn)
    st.plotly_chart(fig_distributions, use_container_width=True)


deploy_footer()

