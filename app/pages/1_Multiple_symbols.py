import pdb
import streamlit as st
import sys  # allows to access to  information used by interpreter , in this case will be used to  point out to the src folder
import os  # allows to interact with the operating system , like checking the paths , catalogs and so on
import plotly.express as px
import altair as alt
from streamlit_autorefresh import st_autorefresh
import plotly.graph_objects as go
import numpy as np

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
import pandas as pd

# Dodaj folder główny projektu do sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from src.api_request_alphavantage import Underlying_request_details
from src.main import main
from src import pipeline
from src import multiple_data_frame
from src import metrics_calcs

import altair as alt


# from src.alpha_vantage_symbols import Symbol_search

# st_autorefresh(interval=500, key="polling") ,  # to be used in the futurue for alpha_vantage_symbol auto population

# os.path.dirname(__file__) - location of the folder where the streamlit_app.py file is, in this case its : app/
# os.path.join(..., '..', 'src') - moving one level higher and pointing out to 'src'
# (os.path.abspath(...) - changing that a full path
# sys.path.append(...) - adding this  folder to places where python needs to search for modules

# Tabs creation

# new_item = Symbol_search()


if "merged_df_one" not in st.session_state:
    st.session_state.merged_df_one = None

if "show_correlation" not in st.session_state:
    st.session_state.show_correlation = False

if "relative_comparison" not in st.session_state:
    st.session_state.relative_comparison = False

    # show_correlation = st.sidebar.checkbox("Correlation", value=False,  key="show_correlation" )


tab0, tab1, tab2, tab3 = st.tabs(["Enter symbol", "Prices", "Charts", "Metrics"])

with tab0:

    if "submit_button" not in st.session_state:
        st.session_state.submit_button = False
    if "selected_symbols" not in st.session_state:
        st.session_state.selected_symbols = []

        # expand / add realtive_coparison

    if "my_list" not in st.session_state:
        st.session_state.my_list = []

    with st.form("add_item_form", clear_on_submit=True):
        new_item = st.text_input("Enter a specfic stock symbol")
        submitted = st.form_submit_button("Add symbol")
        new_item_upper = new_item.upper()
    if submitted and new_item_upper:
        if new_item_upper in st.session_state.my_list:
            pass
        else:
            st.session_state.my_list.append(new_item_upper)

    st.markdown("Once you are completed , please  hit **Submit button**")

    if st.session_state.my_list:
        if st.button("Submit", key="submit_btn"):
            # print("tutaj",st.session_state.my_list)
            st.session_state.submit_button = True
            main()

with tab1:
    with st.sidebar:
        st.title("Symbols")
        # st.session_state.my_list
        # st.markdown("Available symbols: ") # seems to be not requred
        for symbol in st.session_state.my_list:
            st.markdown(f"- {symbol}")
        # selected_symbols=st.multiselect(
        #     'Select your symbols',st.session_state.my_list)

    if st.session_state.submit_button:  # checking if submit button exists
        # pdb.set_trace()
        with st.sidebar:
            st.session_state.selected_symbols = st.multiselect(
                "Select symbols",
                st.session_state.my_list,
                default=st.session_state.selected_symbols,
                key="symbols_multiselect",
            )

        # print("st.session_state.selected_symbols", st.session_state.selected_symbols)
        # print("st.multiselect", st.multiselect)

    if len(st.session_state.selected_symbols) >= 1:
        # take the object  Dataframe_combine_builder from pipeline.multiple_dicts
        single_stock_prices = pipeline.multiple_dicts.get_the_right_dict(
            "single_prices"
        )
        stock_dict = (
            single_stock_prices.single_stock_data
        )  # tihs is now a dict, where I can iterate using symbols

        # Below for dev / debug purpose
        # print(type(stock_dict))
        # for key,value in stock_dict.items():
        #     print(f'key {key}, value : {value}')

        my_symbols = st.session_state.selected_symbols
        symbol_df_builder = pipeline.Dataframe_combine_builder()
        df_list = symbol_df_builder.list_merger(stock_dict, my_symbols)

        # merge those by columns
        if df_list:
            st.session_state.merged_df_one = pd.concat(df_list, axis=1)
            print("sample_merged_list")
            print(st.session_state.merged_df_one)
            st.dataframe(st.session_state.merged_df_one, width="stretch")
        else:
            st.warning("No data for symbols")

    if st.session_state.submit_button and len(st.session_state.selected_symbols) >= 1:
        with st.sidebar:
            st.title(":small[Charts]")
            if (
                st.session_state.submit_button
                and len(st.session_state.selected_symbols) >= 2
            ):
                relative_comparison = st.sidebar.checkbox(
                    "Relative comparison", value=False, key="relative_comparison"
                )
            st.title(":small[Metrics]")
            if (
                st.session_state.submit_button
                and len(st.session_state.selected_symbols) >= 2
            ):
                show_correlation = st.sidebar.checkbox(
                    "Correlation", value=False, key="show_correlation"
                )

    # logic below for correlation calc and display


with tab2:
    if st.session_state.relative_comparison is False:
        for symbol in st.session_state.selected_symbols:
            if st.session_state.merged_df_one is not None:
                df_plot_multi = st.session_state.merged_df_one.reset_index().rename(
                    columns={"index": "Date"}
                )

                fig = px.line(
                    df_plot_multi,
                    x="Date",
                    y=f"{symbol}",
                    labels={f"{symbol}": ""},
                    title=f"Single stock price for: {symbol}",
                )
                st.plotly_chart(fig, use_container_width=True)

    elif st.session_state.relative_comparison is True:

        pass 

    # below to be repalced in the future 
        # --- przykładowe dane ---
        # przykładowe dane
        # df = pd.DataFrame({
        #     "Date": pd.date_range(start="2025-01-01", periods=7),
        #     "Series_A": [100, 105, 102, 110, 115, 120, 125],
        #     "Series_B": [200, 195, 198, 205, 210, 220, 230]
        # })

        # # przelicz na procenty względem pierwszej wartości
        # df_relative = df.copy()
        # for col in ["Series_A", "Series_B"]:
        #     df_relative[col] = df[col] / df[col].iloc[0] * 100

        # df_melted = df_relative.melt(id_vars="Date", var_name="Series", value_name="Value")

        # # --- wykres Altair z dokładnym zakresem dat ---
        # chart = alt.Chart(df_melted).mark_line(point=True).encode(
        #     x=alt.X('Date:T', scale=alt.Scale(domain=[df["Date"].min(), df["Date"].max()])),
        #     y='Value:Q',
        #     color='Series:N',
        #     tooltip=['Date:T', 'Series:N', 'Value:Q']
        # ).properties(
        #     title="Relative Comparison (%)",
        #     width=700,
        #     height=400
        # ).interactive()

        # st.altair_chart(chart, use_container_width=True)
        # ✅ Co robi powyższy fragment:
# # tradingview_html = f"""
# <!-- TradingView Widget BEGIN -->
# <div class="tradingview-widget-container">
# <div id="tradingview_chart"></div>
# <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
# <script type="text/javascript">
# new TradingView.widget({{
#     "width": "100%",
#     "height": 600,
#     "symbol": "{df_single_price}",
#     "interval": "D",
#     "timezone": "Europe/Warsaw",
#     "theme": "light",
#     "style": "1",
#     "locale": "pl",
#     "toolbar_bg": "#f1f3f6",
#     "enable_publishing": false,
#     "withdateranges": true,
#     "hide_side_toolbar": false,
#     "allow_symbol_change": true,
#     "container_id": "tradingview_chart"
# }});
# </script>
# </div>
# <!-- TradingView Widget END -->
# """

# st.components.v1.html(tradingview_html, height=600)

# elif df_single_price is None:
#     print("Missing data")


with tab3:
    if st.session_state.show_correlation is True:
        single_timeframe_returns = pipeline.multiple_dicts.get_the_right_dict(
            "single_timeframe_returns"
        )
        timeframe_returns_dict = single_timeframe_returns.single_stock_data

        # my_symbols
        symbol_df_builder = pipeline.Dataframe_combine_builder()
        df_list = symbol_df_builder.list_merger(stock_dict, my_symbols)
        # merge those by columns
        if df_list:
            merged_df_sec = pd.concat(df_list, axis=1)
            correlation_builder = metrics_calcs.Underlying_metrics.calc_correlation(
                merged_df_sec
            )
            st.markdown("Calculated correlation is:")
            st.dataframe(correlation_builder, width="stretch")

# if st.session_state.submit_button and len(st.session_state.selected_symbols) >= 1:
#     show_worst_best = st.sidebar.checkbox("Worst and Best", value=False)
#     if show_worst_best is True:


# logic for Worst and Best Underlying


# adding some new  checklist button like "Visuals"
#   - normal price graphs
#   -


# https://docs.streamlit.io/develop/api-reference/text/st.markdown

# https://emojipedia.org/laptop
