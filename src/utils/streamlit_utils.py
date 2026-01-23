import streamlit as st
from src.utils import data_finhub_websocket

# from src.api_providers.finhub.finhub_python import Finhub_data_builder
import os
from dotenv import load_dotenv
from pathlib import Path
import logging


# expand with last close
def view_market_data(title, data_requested, quotes):
    with st.expander(title, expanded=True):
        # if st.session_state.websocket is True:
        cols = st.columns(len(data_requested))
        for i, s in enumerate(data_requested):
            symbol_name = data_finhub_websocket.find_the_right_name(s)
            value = quotes.get(s)
            # if st.session_state.set_of_last_close_prices is not None:
            #     last_close=st.session_state.set_of_last_close_prices.get(s)
            #     print(f'last_close:{last_close}')
            #     print(type(last_close))
            # else:
            #     last_close='loading last close price'

            if value is None:
                value = "loading values"
            with cols[i]:
                st.subheader(symbol_name)
                st.write(value)
                # st.write("return=(value - last_close)/last_close")

                # ta metode rozszerzyc o last close, i stope zwrotu



def key_validation(path, api_key_name):
    try:
        api_key = st.secrets[api_key_name]
        logging.info(f"{api_key_name}:{api_key}")
        return api_key

    except Exception:
        load_dotenv(path)
        api_key = os.getenv(api_key_name)
        api_key_to_str = str(api_key)
        logging.info(f"dev_environment: {api_key_name}:{api_key_to_str}") # for dev purpose
        return api_key_to_str
