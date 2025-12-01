import streamlit as st
import numpy as np
import pandas as pd
from src import pipeline
from src import metrics_calcs
from src.utils import data_finhub_websocket
from src import finhub_websocket


def correlation_helper(df_list):
    merged_df_sec = pd.concat(df_list, axis=1)
    correlation_summary = metrics_calcs.Underlying_metrics.calc_correlation(
        merged_df_sec
    )
    return correlation_summary



# method below helps to build and present in a user friendly / readable way data fro websocket

def view_market_data(title, data_requested, quotes):
    with st.expander(title, expanded=True):
        if st.session_state.websocket is True:
            cols = st.columns(len(data_requested))
            for i, s in enumerate(data_requested):
                symbol_name = data_finhub_websocket.find_the_right_name(s)
                value = quotes.get(s)
                if value is None:
                    value = "loading values"
                with cols[i]:
                    st.subheader(symbol_name)
                    st.write(value)
