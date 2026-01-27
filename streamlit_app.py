import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path

# ---- Plausible Analytics ----
components.html(
    """
<!-- Privacy-friendly analytics by Plausible -->
<script async src="https://plausible.io/js/pa-lJvFYtpXWgW5ZoApoiuXh.js"></script>
<script>
  window.plausible = window.plausible || function() { (plausible.q = plausible.q || []).push(arguments) };
  plausible.init = plausible.init || function(i) { plausible.o = i || {} };
  plausible.init()
</script>
""",
    height=0,
)  # height=0, żeby nie zajmował miejsca w UI
# ------------------------------

DEMO_PATH = Path(__file__).parent / "streamlit_assets" / "demo_financial_dashboard.mp4"

DEMO_PATH_SUBTITLES = Path(__file__).parent / "streamlit_assets" / "demo_financial_dashboard.srt"


st.markdown(
    """
# 📊 Financial Dashboard

Welcome! This page provides an overview of the available modules in the application.

---

## 🧭 Project Information
Contains general information about the project:
- **About the author**
- **Project README** and usage instructions
- **BPMN diagram** presenting the system architecture
- **Demo** below:
---
"""
)
with st.expander("▶ Watch demo (1 min)", expanded=True):
    if DEMO_PATH.exists():
        st.video(DEMO_PATH,subtitles=DEMO_PATH_SUBTITLES)
        st.caption(
            "Short demo presenting multi-instrument selection, historical data analysis, correlations, and benchmark metrics."
        )
    else:
        st.warning("Demo vidoe not available")


st.markdown(
    """
## 📈 Live Prices
Real-time market prices provided by **OANDA**, representing CFD instruments across selected asset classes.

---

## 🔍 Multiple Symbols
Allows users to:
- Choose a **data provider / broker**
- Search and analyze multiple financial instruments  
Detailed usage is described in the **README** section.

---

## 📊 Benchmark Metrics
Enables calculation of financial metrics for user-selected symbols compared against:
- Market benchmarks, represented by ETFs referencing major market indices.  
Detailed usage is described in the **README** section.

---

## 📝 Feedback
A simple feedback form allowing users to:
- Select a category
- Send a free-form message to the author (optional)
"""
)
