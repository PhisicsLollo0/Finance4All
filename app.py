import streamlit as st
from pathlib import Path


st.set_page_config(layout="wide", page_title="Finance4All", page_icon="📈")

with st.sidebar.container():
    logo_path = Path(__file__).parent / "logo.png"
    st.image(logo_path, use_container_width=True)


st.title("📈 Finance4All")



st.markdown("""
Welcome to **Finance4All** — your personal investment dashboard.

Use the sidebar to:
- View **Rolling Returns**
- Compare Portfolios
- Analyze Risk
""")
