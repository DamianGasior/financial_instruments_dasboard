import pdb
import streamlit as st
import sys  # allows to access to  information used by interpreter , in this case will be used to  point out to the src folder
import os  # allows to interact with the operating system , like checking the paths , catalogs and so on

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
import pandas as pd

# Dodaj folder główny projektu do sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)
import streamlit as st

st.set_page_config(page_title="Financial Dashboard", layout="wide")

st.title("💰 Financial Dashboard")
st.markdown("Welcome in the application to analize single stocks / etfs and more")

st.info("Use menu on the left to navigate")



