import pdb
import streamlit as st
import sys  # allows to access to  information used by interpreter , in this case will be used to  point out to the src folder
import os  # allows to interact with the operating system , like checking the paths , catalogs and so on
import plotly.express as px
import altair as alt
from streamlit_autorefresh import st_autorefresh
import plotly.graph_objects as go
import numpy as np
from src.api_providers.common.multiple_data_frame import Dataframe_combine_builder

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
import pandas as pd
import logging


from src.main import main

from src.pipeline import pipeline

# from src.pipeline.pipeline import DataPipeline
from src.api_providers.common import multiple_data_frame
from src.metrics import metrics_calcs
from src.metrics import numpy_calcs
from src.api_providers.alpha_vantage import single_data_frame
from src.api_providers.twelve_data import api_request_twelve_data

# from src.utils.main_utils import combined_lists
# from src.utils.streamlit_utils import correlation_helper
import altair as alt
from src.session_init import init_session_state

# Dodaj folder główny projektu do sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

# from src.api_providers.alpha_vantage.api_request_alphavantage import Underlying_request_details
# from src.api_providers.alpha_vantage.single_data_frame import Underlying_data_frame


# from src.alpha_vantage_symbols import Symbol_search

# st_autorefresh(interval=500, key="polling") ,  # to be used in the futurue for alpha_vantage_symbol auto population

# os.path.dirname(__file__) - location of the folder where the streamlit_app.py file is, in this case its : app/
# os.path.join(..., '..', 'src') - moving one level higher and pointing out to 'src'
# (os.path.abspath(...) - changing that a full path
# sys.path.append(...) - adding this  folder to places where python needs to search for modules


init_session_state()


# st.write("PAGE:", __file__)  # this is for debugging purpose for dev work, shows the state of  all st.states
# st.write(st.session_state)   # this is for debugging purpose for dev work , shows the state of  all st.states

# st.session_state.my_benchmarks = ["SPY", "QQQ", "EEM", "GLD"]

st.session_state.my_benchmarks = ["SPY", "QQQ"]

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "Dealer selection",
        "Enter symbol",
        "Prices",
        "Charts",
        "Basic symbol information",
        # "Benchmark metrics",
    ]
)
with tab1:
    st.markdown("Choose one of the data providers")
    broker_selection = st.radio(
        "Select broker", ["Alpha vantage", "Twelve data"], index=1
    )
    st.session_state.selected_broker = broker_selection
    st.markdown(
        "Once you selected the data  provider, go to the next tab : 'Enter symbol'"
    )

with tab2:
    if st.session_state.selected_broker == "Alpha vantage":
        with st.form("add_item_form", clear_on_submit=True):
            new_item = st.text_input("Enter a specfic stock symbol")
            # if st.session_state.selected_broker =="Twelve data":
            #     # users_input=api_request_twelve_data.Underlying_twelve_data_reuquest.symbol_search(new_item)
            submitted = st.form_submit_button("➕ Add symbol")
            new_item_upper = new_item.upper()
        if submitted and new_item_upper:
            if new_item_upper in st.session_state.my_list:
                pass
            else:
                st.session_state.my_list.append(new_item_upper)
    elif st.session_state.selected_broker == "Twelve data":
        st.info(
            "Search engine is available only for  a limited number of  following instruments : forex, cryptos and US listed stock and etf's"
        )

        query = st.text_input("Type your symbol/name of the instrument you are looking for: ")
        if len(query) >= 2:
            symbols_response = (
                api_request_twelve_data.Underlying_twelve_data_reuquest.symbol_search(
                    query
                )
            )

            if not symbols_response:
                st.warning(
                    f'No reposne with your input: "{query}". Try another combination with your input plus something else'
                )
                st.stop()
            elif symbols_response:
                # options=[]
                # for item in symbols_response:
                #     text=f'symbol : {item['symbol']}, instrument_name: {item['instrument_name']},exchange : {item['exchange']}'
                #     options=options.append(text)

                selected = st.selectbox(
                    "Choose one of your instruments from the drop down list . Once you have the right instrument hit '+ Add symbol' ",
                    options=list(
                        symbols_response.keys()
                    ),  # you present to the user only  the keys,
                    key="select_symbols",
                )

                if st.button("➕ Add symbol"):

                    # selected=list(selected.keys())
                    # selected=selected[0]
                    # print(type(selected))
                    # print(selected)
                    value = symbols_response[selected]
                    symbol_ric = value.get("symbol")
                    if symbol_ric not in st.session_state.symbols_for_my_list:
                        st.session_state.symbols_for_my_list.append(symbol_ric)

                # st.session_state.working_list=st.session_state.symbols_for_my_list

                # new_list = []
                # for s in st.session_state.my_list:
                #     if s in st.session_state.symbols_for_my_list:
                #         new_list.append(s)

                # st.session_state.my_list = new_list
                st.info(
                    "Once you finish to look for all your symbols, choose the one below for which you want to request data"
                )
                st.multiselect(
                    "Select symbols for which you want request data:",
                    options=st.session_state.symbols_for_my_list,
                    key="my_list",  # key links this widdget under a specifc key in memorey, key allows to idenfitfy the widget
                    # when a symbol is chosen, then it stays in the default after each script rerun
                )

                # https://chatgpt.com/c/696410bb-d2ac-8333-ba05-e9d79e612d0a

    price_type = st.radio(
        "Select price interval:", ["daily", "weekly", "monthly"], index=0
    )

    st.session_state.users_price_type = price_type

    price_adjustment = st.radio(
        "Select price type:", ["adjusted", "non-adjusted"], index=0
    )

    # to change the value from defaulf , if the use  will choose  "adjusted"
    st.session_state.price_adjustment = price_adjustment

    if st.session_state.selected_broker == "Alpha vantage":

        if price_adjustment == "non-adjusted":
            if price_type == "daily":
                st.session_state.price_type = "TIME_SERIES_DAILY"
            elif price_type == "weekly":
                st.session_state.price_type = "TIME_SERIES_WEEKLY"
            elif price_type == "monthly":
                st.session_state.price_type = "TIME_SERIES_MONTHLY"
        elif price_adjustment == "adjusted":
            if price_type == "daily":
                st.session_state.price_type = "TIME_SERIES_DAILY_ADJUSTED"
            elif price_type == "weekly":
                st.session_state.price_type = "TIME_SERIES_WEEKLY_ADJUSTED"
            elif price_type == "monthly":
                st.session_state.price_type = "TIME_SERIES_MONTHLY_ADJUSTED"

    elif st.session_state.selected_broker == "Twelve data":
        if price_adjustment == "non-adjusted":
            st.session_state.price_type = "none"
        elif price_adjustment == "adjusted":
            st.session_state.price_type = "all"

        if price_type == "daily":
            st.session_state.price_type = "1day"
        elif price_type == "weekly":
            st.session_state.price_type = "1week"
        elif price_type == "monthly":
            st.session_state.price_type = "1month"

    st.markdown("Once you are completed , please  hit **Submit button**")

    
    
    if st.button("Submit"):
        st.session_state.submit_button = True
        st.session_state.my_merged_list = Dataframe_combine_builder.combined_lists(
            st.session_state.my_list, st.session_state.my_benchmarks
        )
        try:
            main()

        except Exception as e:
            logging.exception("App crashed")  # traceback for terminal
            st.error(f"API error: {e}")  # only this will be viisble in UI
            st.stop()

if st.session_state.submit_button:
    with tab3:
        # with st.sidebar:
            # st.title("Symbols")
            # for symbol in st.session_state.my_list:
            #     st.markdown(f"- {symbol}")

        if st.session_state.submit_button:  # checking if submit button is True
            with st.sidebar:
                st.multiselect(
                    "Select symbols",
                    options=st.session_state.my_merged_list,
                    # key="symbols_multiselect", # after I came back from Bencmhar metrics tab , all the requested symbols do dissapear from my tab,
                    key="ui_selected_symbols",
                )
                
        if st.session_state.selected_symbols != st.session_state.ui_selected_symbols:
            st.session_state.selected_symbols = st.session_state.ui_selected_symbols.copy()

        if (
            st.session_state.selected_broker == "Alpha vantage"
            or st.session_state.selected_broker == "Twelve data"
        ):
            if len(st.session_state.selected_symbols) >= 1:
                # take the object  Dataframe_combine_builder from pipeline.multiple_dicts

                single_stock_prices = st.session_state.multi_builder.get_the_right_dict(
                    "single_prices"
                )

                st.session_state.single_stock_prices = single_stock_prices

                # Below for dev / debug purpose
                # print(type(stock_dict))
                # for key,value in stock_dict.items():
                #     print(f'key {key}, value : {value}')

                my_symbols = st.session_state.selected_symbols
                symbol_df_builder = multiple_data_frame.Dataframe_combine_builder()
                df_list = symbol_df_builder.list_merger(
                    st.session_state.single_stock_prices, my_symbols
                )
                print(df_list)
                print("test_df_list")

                # merge those by columns
                if df_list:
                    merged_lists = multiple_data_frame.Dataframe_combine_builder()
                    st.session_state.merged_df_one, message = (
                        merged_lists.list_concacenate(df_list)
                    )
                    print(st.session_state.merged_df_one)
                    st.dataframe(st.session_state.merged_df_one, width="stretch")
                    if message is not None:
                        st.warning(message)

                    print(st.session_state.merged_df_one.to_string())
                    # st.session_state.merged_df_one.show_content()
                else:
                    st.warning("No data for symbols")

            if (
                st.session_state.submit_button
                and len(st.session_state.selected_symbols) >= 1
            ):
                with st.sidebar:
                    st.title(":small[Basic symbol information]")
                    if st.session_state.submit_button:
                        if len(st.session_state.selected_symbols) >= 1:
                            show_stock_profile = st.sidebar.checkbox(
                                "Companies profile",
                                value=False,
                                key="show_stock_profile",
                            )
                            show_basic_numbers = st.sidebar.checkbox(
                                "Basic numbers", value=False, key="show_basic_numbers"
                            )
                            if len(st.session_state.selected_symbols) >= 2:
                                show_correlation = st.sidebar.checkbox(
                                    "Correlation", value=False, key="show_correlation"
                                )

    with tab4:
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
            st.write("Still under development. Plesae be patient..")
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

    with tab5:
        if (
            st.session_state.selected_broker == "Alpha vantage"
            or st.session_state.selected_broker == "Twelve data"
        ):

            if len(st.session_state.selected_symbols) >= 1:
                len_of_selected_symbols = len(st.session_state.selected_symbols)
            else:
                len_of_selected_symbols = 1
            cols = st.columns(len_of_selected_symbols)

            if len(st.session_state.selected_symbols) >= 1:

                if st.session_state.show_basic_numbers is True:
                    print()

                    # print("dlugosc_listy", len(single_timeframe_returns))
                    # for i in single_timeframe_returns:
                    #     print(i)
                    #     print(type(i))

                    columns = st.session_state.merged_df_one.columns

                    price_array, dates_price_array = (
                        numpy_calcs.Numpy_metrics_calcs.to_numpy(
                            st.session_state.merged_df_one
                        )
                    )

                    # merged_df_array=np.asarray(merged_df_array,dtype=float)
                    calc_array = numpy_calcs.Numpy_metrics_calcs(price_array)

                    for i, s in enumerate(st.session_state.selected_symbols):
                        with cols[i]:
                            # add here a function which will pull the start and end date frm the dataframe
                            st.markdown(f"### Stock symbol : {s}")

                            start_date = multiple_data_frame.Dataframe_combine_builder.first_date(
                                st.session_state.merged_df_one
                            )
                            end_date = (
                                multiple_data_frame.Dataframe_combine_builder.last_date(
                                    st.session_state.merged_df_one
                                )
                            )

                            last_price = calc_array.price_last(price_array[:, i])
                            first_price = calc_array.price_first(price_array[:, i])

                            st.write(f"📅End date : {end_date} | Price : {last_price}")
                            st.write(
                                f"📅Start date : {start_date} | Price : {first_price}"
                            )

                            cumulat_return = calc_array.cumulative_return(
                                price_array[:, i]
                            )
                            # st.write(f"Cumulative return for given period : {cumulat_return} %")
                            st.metric(
                                label="Cumulative return for given period",
                                value=f"{(cumulat_return * 100):.4f} %",
                            )

                            # st.write(f"Last price : {last_price}")
                            st.metric(label="Last close price", value=last_price)

                            price_min = calc_array.min_calc(price_array[:, i])
                            # st.write(f"Min : {price_min}")
                            st.metric(label="Min price", value=f"{price_min}")

                            price_max = calc_array.max_calc(price_array[:, i])
                            # st.write(f"Max : {price_max}")
                            st.metric(label="Max pice", value=price_max)

                            return_min = calc_array.daily_return(price_array[:, i])
                            return_min = calc_array.min_calc(return_min) * 100
                            # st.write(f"Min : {price_min}")
                            st.metric(
                                label=f"Min {price_type} return",
                                value=f"{return_min:.4f} %",
                            )

                            return_max = calc_array.daily_return(price_array[:, i])
                            return_max = calc_array.max_calc(return_max) * 100
                            # st.write(f"Min : {price_min}")
                            st.metric(
                                label=f"Max {price_type} return",
                                value=f"{return_max:.4f} %",
                            )

                            price_mean = calc_array.mean_calc(price_array[:, i])
                            # st.write(f"Mean : {price_mean}")
                            st.metric(label="Mean Price", value=price_mean)

                            mean_daily_return = calc_array.return_calcs_mean(
                                price_array[:, i]
                            )
                            # st.write(f"Mean daily return(%): {mean_daily_return}")
                            st.metric(
                                label=f"Mean {price_type} return",
                                value=f"{mean_daily_return * 100:.4f} %",
                            )

                            median_daily_return = calc_array.return_calcs_median(
                                price_array[:, i]
                            )
                            # st.write(f"Mean daily return(%): {mean_daily_return}")
                            st.metric(
                                label=f"Median {price_type} return",
                                value=f"{median_daily_return * 100:.4f} %",
                            )

                            return_st_dev = calc_array.st_dev_calc(price_array[:, i])
                            return_st_dev = return_st_dev * 100
                            st.metric(
                                label=f"{price_type.capitalize()} standard deviation",
                                value=f"{return_st_dev:.4f} %",
                            )

                if st.session_state.show_stock_profile is True:
                    single_company_info = (
                        st.session_state.finhub_info.get_the_right_dict(
                            "single_company_info"
                        )
                    )
                    for i, s in enumerate(st.session_state.selected_symbols):
                        with cols[i]:

                            # print(type(single_company_info))
                            # print("SYBMOL", s)

                            value = single_company_info.get(s)
                            # print(value)
                            # print(type(value))

                            value_df = pd.DataFrame(
                                value.items(), columns=["Label", "Value"]
                            )
                            st.markdown(f"Symbol: {s}")
                            st.dataframe(value_df, hide_index=True, width="stretch")

            if st.session_state.show_correlation is True:
                # df_list = symbol_df_builder.list_merger(stock_dict, my_symbols) # seem to be not required
                # merge those by columns
                if df_list:
                    correlation_builder = multiple_data_frame.Dataframe_combine_builder.correlation_helper(
                        df_list
                    )
                    st.markdown("Calculated correlation is:")
                    st.dataframe(correlation_builder, width="stretch")

    # with tab4:

    #     if st.session_state.submit_button:  # checking if submit button exists
    #         with st.sidebar:
    #             st.session_state.select_benchmarks = st.multiselect(
    #                 "Select benchmarks",
    #                 st.session_state.my_benchmarks,
    #                 default=st.session_state.select_benchmarks,
    #                 key="symbols_multiselect_benchmarks",
    #             )

    #     if (
    #         st.session_state.submit_button
    #         and len(st.session_state.selected_symbols) >= 1
    #         and len(st.session_state.select_benchmarks) >= 1
    #     ):
    #         with st.sidebar:
    #             st.title(":small[Benchmark metrics]")
    #             if (
    #                 st.session_state.submit_button
    #                 and len(st.session_state.selected_symbols) >= 1
    #             ):
    #                 show_correlation_benchmark = st.sidebar.checkbox(
    #                     "Correlation", value=False, key="show_correlation_benchmark"
    #                 )

    #     if st.session_state.show_correlation_benchmark is True:
    #         my_symbols_merged = Dataframe_combine_builder.combined_lists(
    #             st.session_state.select_benchmarks, st.session_state.selected_symbols
    #         )
    #         df_list_with_benchmark = symbol_df_builder.list_merger(
    #             single_stock_prices, my_symbols_merged
    #         )

    #         # df_list_with_benchmark_returns=

    #         df_list_returns = metrics_calcs.Underlying_metrics.price_chng_perct_for_list(
    #             single_stock_prices, my_symbols_merged
    #         )
    #         # df_list_returns_reviewed=multiple_data_frame.Dataframe_combine_builder.correlation_helper()
    #         if df_list_with_benchmark:
    #             correlation_builder = (
    #                 multiple_data_frame.Dataframe_combine_builder.correlation_helper(
    #                     df_list_returns
    #                 )
    #             )
    #             # correlation_builder = multiple_data_frame.Dataframe_combine_builder.correlation_helper(df_list_returns_reviewed)

    #             st.markdown("Calculated correlation is:")
    #             st.dataframe(correlation_builder, width="stretch")
    #             with st.expander(" Pearson Correlation (r) definition, click to expand"):
    #                 st.write(
    #                     """
    #                         What does it measure?
    #                         How strongly and linearly two instruments move together.
    #                         Range: from –1 to +1.

    #                         +1 → they move in the same direction, perfectly

    #                         0 → no linear relationship

    #                         –1 → they move in opposite directions

    #                         Most important: Correlation tells you only about the direction and consistency of movement, but not how many units something increases or decreases.

    #                         Example:
    #                         If the S&P 500 goes up by 1% → Apple often also goes up by around 1%
    #                         → high correlation (e.g., 0.9)
    #                         But we still don’t know whether Apple increases more or less.
    #                 """
    #                 )

    # if st.session_state.submit_button and len(st.session_state.selected_symbols) >= 1:
    #     show_worst_best = st.sidebar.checkbox("Worst and Best", value=False)
    #     if show_worst_best is True:

    # logic for Worst and Best Underlying

    # adding some new  checklist button like "Visuals"
    #   - normal price graphs
    #   -

    # https://docs.streamlit.io/develop/api-reference/text/st.markdown

    # https://emojipedia.org/laptop
