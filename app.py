import streamlit as st

def main():

    st.set_page_config(layout="wide", page_title="Finance4All", page_icon="📈")

    st.title("📈 Finance4All")
    st.markdown("""
    Welcome to **Finance4All** — your personal investment dashboard.

    Use the sidebar to:
    - View **Rolling Returns**
    - Compare Portfolios
    - Analyze Risk
    """)

if __name__ == "__main__":
    main()