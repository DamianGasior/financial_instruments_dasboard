import streamlit as st
import streamlit.components.v1 as components

# ---- Plausible Analytics ----
components.html("""
<!-- Privacy-friendly analytics by Plausible -->
<script async src="https://plausible.io/js/pa-lJvFYtpXWgW5ZoApoiuXh.js"></script>
<script>
  window.plausible = window.plausible || function() { (plausible.q = plausible.q || []).push(arguments) };
  plausible.init = plausible.init || function(i) { plausible.o = i || {} };
  plausible.init()
</script>
""", height=0)  # height=0, żeby nie zajmował miejsca w UI
# ------------------------------



st.title("Financial Dashboard")
st.write("Welcome, go the the tabs on the left, start from the top left👈")