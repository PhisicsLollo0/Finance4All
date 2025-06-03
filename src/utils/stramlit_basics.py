import streamlit as st
from pathlib import Path

def deploy_sidebar_menu():
    with st.sidebar.container():
        logo_path = Path(__file__).parent.parent.parent / "logo.png"
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

def deploy_footer():
    st.markdown("---")
    st.caption("© 2025 Finance4All – MIT License | Built with ❤️ using Streamlit")
    st.caption("Connect with me:")
    st.caption("[GitHub](https://github.com/PhisicsLollo0/Finance4All) | [LinkedIn](https://www.linkedin.com/in/lorenzo-cavallo/)")