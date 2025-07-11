import streamlit as st
import pandas as pd

from src.utils.stramlit_basics import deploy_sidebar_menu, deploy_footer

# Set page config
st.set_page_config(
    page_title="Finance4All – Passive Investing Guide",
    page_icon="💰",
    layout="wide"
)

# === Sidebar ===
deploy_sidebar_menu()

# === Main Content ===
st.title("💰 Passive Investing: A Practical Guide")

st.markdown("""
Passive investing is an investment strategy aimed at maximizing returns by minimizing buying and selling activities. It typically involves investing in index funds or ETFs.

### Benefits of Passive Investing:
- Lower costs
- Reduced risk through diversification
- Simplicity and transparency
- Long-term wealth accumulation

---
""")

# === Interactive Example: Impact of Fees on Investments ===
st.header("💸 Fees Impact Calculator")

col1, col2, col3 = st.columns(3)

initial_investment = col1.number_input("Initial Investment ($)", value=10000, step=1000)
annual_contribution = col2.number_input("Annual Contribution ($)", value=1000, step=500)
years = col3.slider("Investment Duration (years)", min_value=1, max_value=50, value=30)

rate_of_return = st.slider("Estimated Annual Rate of Return (%)", min_value=1.0, max_value=15.0, value=7.0, step=0.1)

fee_classes = {
    "No Fees (Fiscal Paradise)": 0.0,
    "Typical ETF (TER ~0.2%)": 0.2,
    "Pension Fund (TER ~1%)": 1.0,
    "Managed Funds (TER ~2.5%)": 2.5
}

# Compound interest calculation with fees
def calculate_investment(initial, annual, rate, fee, years):
    values = []
    total = initial
    for year in range(1, years + 1):
        total = (total + annual) * (1 + (rate - fee) / 100)
        values.append(total)
    return values

investment_results = {}
for fee_name, fee_rate in fee_classes.items():
    investment_results[fee_name] = calculate_investment(initial_investment, annual_contribution, rate_of_return, fee_rate, years)

df_fees_impact = pd.DataFrame(investment_results, index=range(1, years + 1))
st.line_chart(df_fees_impact)

final_amounts = {key: value[-1] for key, value in investment_results.items()}
st.markdown("### Investment Outcome After Fees")
for fee_name, amount in final_amounts.items():
    st.markdown(f"- **{fee_name}:** ${amount:,.2f}")

# === Example Portfolio ===
st.header("🗂️ Example Passive Investment Portfolio")

portfolio_data = {
    "Asset": ["S&P 500 ETF", "International ETF", "Bond ETF", "Real Estate ETF"],
    "Allocation (%)": [50, 20, 20, 10]
}
df_portfolio = pd.DataFrame(portfolio_data)

st.table(df_portfolio)

st.markdown("""
A diversified portfolio typically includes a balanced allocation across different asset classes to spread risk effectively.
""")

# Footer
deploy_footer()