import streamlit as st
from pathlib import Path
import base64

# Set page config
st.set_page_config(
    page_title="Finance4All – Home",
    page_icon="🏠",
    menu_items=None,
    layout="centered",
)

# === Sidebar logo ===
with st.sidebar.container():
    logo_path = Path(__file__).parent / "logo.png"
    if logo_path.exists():
          st.image(logo_path, use_container_width=True)

# Clickable links to different pages
st.sidebar.page_link("🏠_Home.py", label="🏠 Home")
st.sidebar.markdown("### 📚 How To Pages")
st.sidebar.page_link("pages/1_🛌_Passive_Investing.py", label="🛌 Passive Investing")

# Separator
st.sidebar.markdown("---")
st.sidebar.markdown("### Simulation & Analysis")
st.sidebar.page_link("pages/2_📈_Rolling_Returns.py", label="📈 Rolling Returns")


# === Main content ===
# Main page logo (if exists)
logo_main_path = Path(__file__).parent / "logo.png"
if logo_main_path.exists():
    with open(logo_main_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
        st.markdown(
            f"""
            <div style="text-align: center;">
                <img src="data:image/png;base64,{encoded_string}" width="500">
            </div>
            """,
            unsafe_allow_html=True
        )

# Disclaimer
st.warning("⚠️ Disclaimer: This project is under active development and is not ready for production use. Features, APIs, and results may change without notice. Use at your own risk.")

# Description
st.markdown("""
**Finance4All** is a Python-based project 🌟 for outreach in personal finance and investment education.

It provides a series of **"How To"** pages 📄 that aim to guide you into the world of personal finance and passive investing.  
To start, it’s better to define these two concepts:

- **Personal Finance** 💰: The management of an individual's financial activities, including budgeting, saving, investing, and planning for future financial goals.  
- **Passive Investing** 🛌: An investment strategy that aims to maximize returns by minimizing buying and selling activities. It typically involves investing in index funds or ETFs that track global market indices.

Currently, the project does not explore the concept of Behavioral Finance 🧠, which is the study of how psychological factors influence financial decision-making. However, since it is a major factor that can affect both returns and psychological well-being, I will consider adding it in the future.

Since I am only a passionate individual 😊, this project is not intended to be a professional financial advisory service. Instead, it is meant to be my personal digital bucket 🪣 that contains all the knowledge I have collected while learning about personal finance and passive investing. Given that, it will contain a lot of resources, articles, and tools not developed by me — in these cases, you will find the source of the resource linked next to it 🔗.

If you want to know more about me and my background, you can check out my website [Lorenzo Cavallo](https://phisicslollo0.github.io/) 🌐.
""")

st.divider()

# App sections
st.header("📑 App Pages")
st.markdown("""
- **🛌 Passive Investig:** Overview of the project, purpose, and key features.
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
