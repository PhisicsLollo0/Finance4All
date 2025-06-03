import streamlit as st
from pathlib import Path

from src.utils.stramlit_basics import deploy_sidebar_menu, deploy_footer

# Set page config
st.set_page_config(
    page_title="Finance4All – Home",
    page_icon="💰",
    layout="wide",
    menu_items=None,
)

# === Sidebar ===
deploy_sidebar_menu()

# === Main content ===
# st.title("💰 Finance4All")

# Footer
deploy_footer()
