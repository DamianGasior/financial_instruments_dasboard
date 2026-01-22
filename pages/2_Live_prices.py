import pdb
import streamlit as st
import sys  # allows to access to  information used by interpreter , in this case will be used to  point out to the src folder
import os  # allows to interact with the operating system , like checking the paths , catalogs and so on
from src.api_providers.finhub import finhub_websocket
import threading
from src.utils import data_finhub_websocket
from src.utils import streamlit_utils



# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
import pandas as pd
import websocket
from src.api_providers.finhub.finhub_websocket import ws_connection
from src.api_providers.finhub.finhub_websocket import finhub_python
from streamlit_autorefresh import st_autorefresh


st_autorefresh(interval=2000)  # co 2 sekundy

# Dodaj folder główny projektu do sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)
import streamlit as st

if "symbol_quotes" not in st.session_state:
    st.session_state.symbol_quotes = {}

if "symbol_quotes_indices" not in st.session_state:
    st.session_state.symbol_quotes_indices = {}

if "symbol_quotes_fx_pairs" not in st.session_state:
    st.session_state.symbol_quotes_fx_pairs = {}

if "symbols_set" not in st.session_state:
    st.session_state.symbols_req_cryptos = []

if "symbols_oanda_indices" not in st.session_state:
    st.session_state.symbols_oanda_indices = []

if "symbols_oanda_ccy_pairs" not in st.session_state:
    st.session_state.symbols_oanda_ccy_pairs = []

if "symbol_quotes_cmdty" not in st.session_state:
    st.session_state.symbol_quotes_cmdty = {}

if "symbol_quotes_bond_yields" not in st.session_state:
    st.session_state.symbol_quotes_bond_yields = {}


if "websocket" not in st.session_state:
    st.session_state.websocket = True
    threading.Thread(
        target=finhub_websocket.start_web_socket, daemon=True
    ).start()  # starting websocket in a seperate thread
    # so that it can work the howle time in the background,
    # daemon=True , once the app will be closed, thread will be clsoed as well

st.set_page_config(page_title="Financial Dashboard", layout="wide")

st.title("💰 Financial Dashboard")
st.markdown("Welcome in the application to analize single stocks / etfs and more")

st.info("Use menu on the left to navigate")


# https://pypi.org/project/websocket_client/
if st.session_state.websocket is True:
    result = finhub_websocket.on_message


if result:
    st.session_state.symbol_quotes = finhub_websocket.symbol_quotes
    st.session_state.symbols_req_cryptos = data_finhub_websocket.symbols_req_cryptos
    st.session_state.symbol_quotes_indices = finhub_websocket.symbol_quotes_indices
    st.session_state.symbols_oanda_indices = data_finhub_websocket.symbols_oanda_indices
    st.session_state.symbols_oanda_bond_yields = (
        data_finhub_websocket.symbols_oanda_bond_yields
    )
    st.session_state.symbols_oanda_ccy_pairs = (
        data_finhub_websocket.symbols_oanda_ccy_pairs
    )
    st.session_state.symbol_quotes_fx_pairs = finhub_websocket.symbol_quotes_fx_pairs
    st.session_state.symbols_oanda_cmdty = data_finhub_websocket.symbols_oanda_cmdty
    st.session_state.symbol_quotes_cmdty = finhub_websocket.symbol_quotes_cmdty
    st.session_state.symbol_quotes_bond_yields = (
        finhub_websocket.symbol_quotes_bond_yields
    )

# st.session_state.set_of_last_close_prices = (
#     finhub_python.Finhub_data_builder.request_for_previous_close(
#         st.session_state.symbols_req_cryptos
#         # st.session_state.symbols_oanda_indices,
#         # st.session_state.symbols_oanda_bond_yields,
#         # st.session_state.symbols_oanda_ccy_pairs,
#         # st.session_state.symbols_oanda_cmdty,
#     )
# )

# st.write("1", st.session_state.symbol_quotes_indices)
# st.write("2", st.session_state.symbol_quotes)
# # st.write("3", st.session_state.symbols_req_cryptos)
# # st.write("4", st.session_state.symbols_oanda_indices)
# st.write("5", st.session_state.symbol_quotes_fx_pairs)
# st.write("6", st.session_state.symbol_quotes_cmdty)
# st.write("7", st.session_state.symbol_quotes_bond_yields)

# else:
#     st.session_state.symbol_quotes = {}
#     st.session_state.symbols_req_cryptos = {}
#     st.session_state.symbol_quotes_indices = {}
#     st.session_state.symbols_oanda_indices = {}
#     st.session_state.symbols_oanda_ccy_pairs = {}
#     st.session_state.symbol_quotes_fx_pairs = {}
#     st.session_state.symbols_oanda_cmdty = {}
#     st.session_state.symbol_quotes_cmdty = {}


# if "symbol_quotes" not in st.session_state:
#     st.session_state.symbol_quotes = {}
#     if not finhub_websocket.symbol_quotes:
#         st.session_state.symbol_quotes == finhub_websocket.symbol_quotes
#         print('finhub_websocket.symbol_quotes',finhub_websocket.symbol_quotes)
#     else:
#         st.session_state.symbol_quotes = {}


# the below is to check if the queue is working correctliny and new itmes are added
# if st.button("Check queue size"):
#     q_size = finhub_websocket.size()
#     st.write(q_size)


# if st.button("Check last_message"):
#     q_last_message = finhub_websocket.get_last_message()
#     st.write(q_last_message)


# if st.button("Check last_quote"):
#     q_last_quote = finhub_websocket.get_specific_symbol()
#     st.write(q_last_quote)
#     st.metric(label=q_last_quote[0], value=q_last_quote[1])


if st.button("Close websocket"):
    finhub_websocket.ws_connection.close()
    st.success("Websocket closing...")


st.title("Real-time prices")

q_last_quote = finhub_websocket.get_specific_symbol()


# if "BINANCE:BTCUSDT" in st.session_state.symbol_quotes:
#     value1 = st.session_state.symbol_quotes["BINANCE:BTCUSDT"]
# else:
#     value1 = "Waiting for quotes"

# # st.write(value1)
# st.metric(label="BINANCE:BTCUSDT", value=value1)


# st.title("Commodities :small[ [Exchange : Symbol] ]")
# # st.subheader("Commodities :small[ [Exchange : Symbol] ]")
# # st.write("Commodities :small[ [Exchange : Symbol] ]")
# # st.markdown("Exchange : Symbol")
# cols = st.columns(len(st.session_state.symbols_oanda_cmdty))
# if st.session_state.websocket is True:
#     for i, s in enumerate(st.session_state.symbols_oanda_cmdty):
#         with cols[i]:
#             st.metric(
#                 label=s,
#                 value=st.session_state.symbol_quotes_cmdty.get(s, "missing quotes"),
# )

if not st.session_state.websocket :
    st.status("Loading prices...", state="running")

elif st.session_state.websocket :
    
    streamlit_utils.view_market_data(
        "Indices",
        st.session_state.symbols_oanda_indices,
        st.session_state.symbol_quotes_indices,
    )

    streamlit_utils.view_market_data(
        "Commodities",
        st.session_state.symbols_oanda_cmdty,
        st.session_state.symbol_quotes_cmdty,
    )

    streamlit_utils.view_market_data(
        "Fx pairs",
        st.session_state.symbols_oanda_ccy_pairs,
        st.session_state.symbol_quotes_fx_pairs,
    )

    streamlit_utils.view_market_data(
        "Bond yields",
        st.session_state.symbols_oanda_bond_yields,
        st.session_state.symbol_quotes_bond_yields,
    )

    streamlit_utils.view_market_data(
        "Cryptos", st.session_state.symbols_req_cryptos, st.session_state.symbol_quotes
    )
