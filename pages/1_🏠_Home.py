import streamlit as st
from pathlib import Path

# Set page config
st.set_page_config(
    page_title="Finance4All – Home",
    page_icon="💰",
    layout="wide"
)

# === Sidebar logo ===
with st.sidebar.container():
    logo_path = Path(__file__).parent.parent / "logo.png"
    if logo_path.exists():
        st.image(logo_path, use_container_width=True)

# === Main content ===
# st.title("💰 Finance4All")

# Disclaimer
st.warning("⚠️ Disclaimer: This project is under active development and is not ready for production use. Features, APIs, and results may change without notice. Use at your own risk.")

# Main page logo (if exists)
logo_main_path = Path(__file__).parent.parent / "logo.png"
if logo_main_path.exists():
    st.image(logo_main_path, width=500)

# Description
st.markdown("""
**Finance4All** is a Python-based toolkit for analyzing, backtesting, and visualizing financial portfolios.

It offers tools for:
- Scraping historical price data
- Computing portfolio returns
- Evaluating risk metrics
- Generating insightful visualizations
""")

st.divider()

# App sections
st.header("📑 App Pages")
st.markdown("""
- **🏠 Home:** Overview of the project, purpose, and key features.
- **📈 Rolling Returns:** Interactive visualization of rolling return metrics across portfolios.
""")

# Features
st.header("🚀 Key Features")
st.markdown("""
- **Data Scraping:** Update and download historical price data for assets.
- **Portfolio Analysis:** Load, clean, and manipulate custom portfolios.
- **Return Computation:** Calculate annualized and rolling returns over user-defined windows.
- **Risk Metrics:** Analyze geometric means, quantiles, and maximum drawdowns.
- **Visualization:** Interactive plots for returns, drawdowns, and rolling performance.
""")

st.divider()

# Project structure
with st.expander("📁 Project Structure"):
    st.code("""
.
├── data/                # Raw and processed data files
├── notebooks/           # Jupyter notebooks for exploration and analysis
├── src/
│   ├── computations/    # Return and risk computations
│   ├── plots/           # Plotting utilities
│   ├── portfolio/       # Portfolio management
│   ├── scraping/        # Data scraping utilities
│   └── utils/           # Misc utilities
├── prices_scraping.ipynb
├── README.md
└── .env
    """, language="text")

# Footer
st.markdown("---")
st.caption("© 2025 Finance4All – MIT License | Built with ❤️ using Streamlit")
