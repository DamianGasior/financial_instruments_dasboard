import streamlit as st
from src.utils import data_finhub_websocket
from src.api_providers.finhub.finhub_python import Finhub_data_builder
from src.session_init import init_session_state


init_session_state()


# method below helps to build and present in a user friendly / readable way data fro websocket


# rozszerzyc o last close
def view_market_data(title, data_requested, quotes):
    with st.expander(title, expanded=True):
        if st.session_state.websocket is True:
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


if "my_merged_list_0" not in st.session_state:
    st.session_state.my_merged_list_0 = []


# def combined_lists(symbols_from_user, benchmarks):
#     merged_test_symbols = []
#     for symbol in symbols_from_user:
#         merged_test_symbols.append(symbol)

#     merged_test_symbols.append(benchmarks)

#     print(merged_test_symbols)
#     return merged_test_symbols
