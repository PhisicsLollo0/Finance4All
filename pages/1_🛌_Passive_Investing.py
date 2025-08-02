import streamlit as st
import pandas as pd

from src.utils.stramlit_basics import deploy_sidebar_menu, deploy_footer

# Set page config
st.set_page_config(
    page_title="Finance4All – Passive Investing Guide",
    page_icon="💰",
    # layout="wide"
)

# === Sidebar ===
deploy_sidebar_menu()

# === Main Content ===
st.title("💰 Passive Investing: A Practical Guide")

st.markdown(""" 
**Passive investing**, much like quantum mechanics, is built upon foundational axioms—assumptions you accept to navigate the landscape ahead. You don’t necessarily have to agree completely, but to invest passively, you accept (at least tentatively) these core beliefs:

1. **Markets are efficient 🏦✨**  
   Prices are _always_ correct and incorporate all available information. This means we don’t have any special edge over the market: trying to beat it through analysis or prediction is (mostly) futile, since any new information is almost instantly reflected in stock prices.

2. **Long-term growth 📈🌱**  
   Over time, human innovation, productivity, and the drive to create value have led to steady economic progress. This ongoing creation of wealth is reflected in market prices, which—despite short-term swings—tend to grow over the long run. 

These two principles form the bedrock of passive investing. If you do not accept them, your journey into passive investing may finish here. However, read the next few lines and give me a chance to convince you.

---
       
### “Markets are efficient” 🏦✨

#### Historical Data
Decades of academic research—including landmark studies like the SPIVA® (S&P Indices Versus Active) reports—consistently reveal that the vast majority of actively managed funds fail to beat their benchmark indexes over time, especially after accounting for fees and taxes. Even professional investors with deep resources and expertise struggle to outperform a simple index-tracking strategy. This body of evidence supports the idea that market efficiency makes it extremely difficult to achieve better-than-market returns through stock picking or market timing.

#### Who Are You Really Competing With?
When you try to beat the market through stock picking or market timing, you’re not just playing a friendly game against casual investors. You are, in fact, competing against some of the world’s largest investment funds and professional institutions—organizations that employ thousands of highly skilled analysts, leverage billions of dollars in research budgets, and operate with cutting-edge technology and privileged access to information.
Beating the market is not their hobby; it’s their full-time job. These institutions dedicate immense resources to finding the smallest market inefficiencies, often acting on new information in seconds. So, before trusting in a single “brilliant” idea or your unique read of a geopolitical event, it’s worth asking: _Are you confident you can outsmart teams whose sole mission is to outperform everyone else—including you?_
            
---

### For “Long-term growth” 📈🌱
Human history is fundamentally a story of **progress**. From the dawn of civilization, people have continuously strived to improve their condition—*inventing new tools, creating better systems, and overcoming countless challenges* along the way. While this path has not always been smooth—periods of stagnation and setbacks are part of our journey—the long-term trend has been one of remarkable advancement.

In the past century especially, we have witnessed an acceleration of growth unlike anything before. ⚡️ Breakthroughs in science, technology, and organization have led to unprecedented leaps in *productivity, efficiency, and overall value creation*. This steady process of innovation is not just a pattern from the past, but a core belief for the future: **humans will keep finding new ways to solve problems, increase productivity, and generate new wealth.**

As a result, the value created by this ongoing progress is ultimately reflected in rising market prices 📈. This is the foundation of the long-term growth axiom in passive investing. Of course, it’s possible that innovation could slow down—or even stop entirely—one day. But *all historical evidence* suggests that the tendency for humans to upgrade themselves and their societies is a fundamental driver of economic and market growth.
""")

import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# --- your session_state + button/toggle setup ---
if "selected_annual_return" not in st.session_state:
    st.session_state.selected_annual_return = 0.07

col1, col2, col3, col4 = st.columns([1.2,1.2,2.,1.3])
with col1:
    if st.button("Stock Market", key="stock_market"):
        st.session_state.selected_annual_return = 0.07
with col2:
    if st.button("Bonds", key="bonds"):
        st.session_state.selected_annual_return = 0.03

options = {
    "Fiscal Paradise":   {"key": "fiscal_paradise", "TER": 0.00,  "default": True},
    "ETF":               {"key": "etf",             "TER": 0.002, "default": False},
    "Retirement Fund":   {"key": "retirement_fund", "TER": 0.01,  "default": False},
    "Banca Inculia":     {"key": "banca_inculia",   "TER": 0.02,  "default": False},
    "Pirats":            {"key": "pirats",          "TER": 0.03,  "default": False}
}

# collect which ones are toggled on
selected = []
for label, cfg in options.items():
    if st.toggle(label, key=cfg["key"], value=cfg["default"]):
        selected.append((label, cfg["TER"]))

with col4:
    for label, ter in selected:
        st.markdown(f"**{label}: {ter*100:.2f}% TER**")

# slider for manual override if you still need it
col5, col6 = st.columns([1,1])
with col5:
    annual_return = st.slider(
        "Annual Expected Return",
        min_value=0.02,
        max_value=0.1,
        value=st.session_state.selected_annual_return,
        step=0.01,
        format="%.2f"
    )

# --- build a combined DataFrame for all selected TERs ---
years = np.arange(0, 41)
df_list = []
for label, ter in selected:
    # simulate starting at 1, growing at (1 + ter) per year
    values = (1 + ter) ** years
    df_list.append(pd.DataFrame({
        "Year": years,
        "Value": values,
        "Option": label
    }))

if df_list:
    df_all = pd.concat(df_list, ignore_index=True)

    # plot
    fig, ax = plt.subplots()
    sns.lineplot(data=df_all, x="Year", y="Value", hue="Option", ax=ax)
    ax.set_title("40‑Year Growth for Selected TERs")
    ax.set_ylabel("Relative Value (start = 1)")
    ax.grid(True)
    st.pyplot(fig)
else:
    st.info("Please toggle at least one TER option to see the simulation.")


# Footer
deploy_footer()