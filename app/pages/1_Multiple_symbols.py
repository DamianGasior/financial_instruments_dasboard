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


from src.main import main

from src.pipeline import pipeline

# from src.pipeline.pipeline import DataPipeline
from src.api_providers.common import multiple_data_frame
from src.metrics import metrics_calcs
from src.metrics import numpy_calcs
from src.api_providers.alpha_vantage import single_data_frame
from src.utils.main_utils import combined_lists
from src.utils.streamlit_utils import correlation_helper
import altair as alt
from src.api_providers.finhub.finhub_python import Finhub_data_builder
from src.metrics.metrics_calcs import Underlying_metrics

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


if "merged_df_one" not in st.session_state:
    st.session_state.merged_df_one = None

if "show_correlation" not in st.session_state:
    st.session_state.show_correlation = False

if "show_stock_profile" not in st.session_state:
    st.session_state.show_stock_profile = False

if "show_basic_numbers" not in st.session_state:
    st.session_state.show_basic_numbers = False

if "relative_comparison" not in st.session_state:
    st.session_state.relative_comparison = False


if "show_mean" not in st.session_state:
    st.session_state.relative_comparison = False

if "submit_button" not in st.session_state:
    st.session_state.submit_button = False

if "selected_symbols" not in st.session_state:
    st.session_state.selected_symbols = []

if "Select_benchmarks" not in st.session_state:
    st.session_state.select_benchmarks = []

if "my_benchmarks" not in st.session_state:
    st.session_state.my_benchmarks = []

    # expand / add realtive_coparison

if "my_list" not in st.session_state:
    st.session_state.my_list = []

if "show_correlation_benchmark" not in st.session_state:
    st.session_state.show_correlation_benchmark = False

if "price_type" not in st.session_state:
    st.session_state.price_type = "TIME_SERIES_DAILY"

if "price_adjustment" not in st.session_state:
    st.session_state.price_adjustment = "non-adjusted"


if "selected_broker" not in st.session_state:
    st.session_state.selected_broker = None

# if "multi_builder" not in st.session_state:
#     st.session_state.multi_builder = Dataframe_combine_builder()

# if "metrics_instance" not in st.session_state:
#     st.session_state.metrics_instance = None

# show_correlation = st.sidebar.checkbox("Correlation", value=False,  key="show_correlation" )


st.session_state.my_benchmarks = ["SPY"]

tab00, tab0, tab1, tab2, tab3, tab4 = st.tabs(
    [
        "Dealer selection",
        "Enter symbol",
        "Prices",
        "Charts",
        "Basic symbol information",
        "Benchmark metrics",
    ]
)
with tab00:
    st.markdown("Choose one of the data providers")
    broker_selection = st.radio(
        "Select broker", ["Alpha vantage", "Alpha vantage_test", "Twelve data"], index=2
    )
    st.session_state.selected_broker = broker_selection
    st.markdown(
        "Once you selected the data  provider, go to the next tab : 'Enter symbol'"
    )

with tab0:

    with st.form("add_item_form", clear_on_submit=True):
        new_item = st.text_input("Enter a specfic stock symbol")
        submitted = st.form_submit_button("Add symbol")
        new_item_upper = new_item.upper()
    if submitted and new_item_upper:
        if new_item_upper in st.session_state.my_list:
            pass
        else:
            st.session_state.my_list.append(new_item_upper)

    price_type = st.radio(
        "Select price interval:", ["daily", "weekly", "monhtly"], index=0
    )

    price_adjustment = st.radio(
        "Select price type:", ["adjusted", "non-adjusted"], index=1
    )

    # to change the value from defaulf , if the use  will choose  "adjusted"
    st.session_state.price_adjustment = price_adjustment

    if price_adjustment == "non-adjusted":
        if price_type == "daily":
            st.session_state.price_type = "TIME_SERIES_DAILY"
        elif price_type == "weekly":
            st.session_state.price_type = "TIME_SERIES_WEEKLY"
        elif price_type == "monhtly":
            st.session_state.price_type = "TIME_SERIES_MONTHLY"
    elif price_adjustment == "adjusted":
        if price_type == "daily":
            st.session_state.price_type = "TIME_SERIES_DAILY_ADJUSTED"
        elif price_type == "weekly":
            st.session_state.price_type = "TIME_SERIES_WEEKLY_ADJUSTED"
        elif price_type == "monhtly":
            st.session_state.price_type = "TIME_SERIES_MONTHLY_ADJUSTED"

    st.markdown("Once you are completed , please  hit **Submit button**")

    st.session_state.my_merged_list = combined_lists(
        st.session_state.my_list, st.session_state.my_benchmarks
    )

    if st.session_state.my_merged_list:

        if st.button("Submit", key="submit_btn"):
            st.session_state.submit_button = True

            main()

    # if st.button("Submit", key="submit_btn"):
    #     st.session_state.submit_button = True
    #     if pipeline.Underlying_data_frame():
    #         test_response = Underlying_request_details.request_to_ext_api()
    #         if test_response == 'Response is from cache.Seems there was already a similar request triggered today' :
    #             st.write('udalo sie2')
    #         elif test_response == 'Response was succesfull (200)' :
    #             st.write('udalo sie1')
    # pipeline.UnderlyingBuilder.run_pipeline.data
    # st.write(pipeline.Underlying_data_frame())

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
        with st.sidebar:
            st.session_state.selected_symbols = st.multiselect(
                "Select symbols",
                st.session_state.my_list,
                default=st.session_state.selected_symbols,
                key="symbols_multiselect",
            )
    # if st.session_state.selected_broker == "Alpha vantage":
    #     if len(st.session_state.selected_symbols) >= 1:
    #         # take the object  Dataframe_combine_builder from pipeline.multiple_dicts
    #         single_stock_prices = st.session_state.multi_builder.get_the_right_dict(
    #             "single_prices"
    #         )
    #         stock_dict = (
    #             single_stock_prices.single_stock_data
    #         )  # tihs is now a dict, where I can iterate using symbols

    #         # Below for dev / debug purpose
    #         # print(type(stock_dict))
    #         # for key,value in stock_dict.items():
    #         #     print(f'key {key}, value : {value}')

    #         my_symbols = st.session_state.selected_symbols
    #         symbol_df_builder = Dataframe_combine_builder()
    #         df_list = symbol_df_builder.list_merger(stock_dict, my_symbols)

    #         # merge those by columns
    #         if df_list:
    #             merged_lists = multiple_data_frame.Dataframe_combine_builder()
    #             st.session_state.merged_df_one = merged_lists.list_concacenate(df_list)
    #             st.dataframe(st.session_state.merged_df_one, width="stretch")
    #         else:
    #             st.warning("No data for symbols")

    #     if (
    #         st.session_state.submit_button
    #         and len(st.session_state.selected_symbols) >= 1
    #     ):
    #         with st.sidebar:
    #             # Leave for later to add some additional options for charts, for now, single charts are fine
    #             # st.title(":small[Charts]")
    #             # if (
    #             #     st.session_state.submit_button
    #             #     and len(st.session_state.selected_symbols) >= 2
    #             # ):
    #             #     relative_comparison = st.sidebar.checkbox(
    #             #         "Relative comparison", value=False, key="relative_comparison"
    #             #     )
    #             st.title(":small[Basic symbol information]")
    #             if st.session_state.submit_button:
    #                 if len(st.session_state.selected_symbols) >= 1:
    #                     show_stock_profile = st.sidebar.checkbox(
    #                         "Companies profile", value=False, key="show_stock_profile"
    #                     )
    #                     show_basic_numbers = st.sidebar.checkbox(
    #                         "Basic numbers", value=False, key="show_basic_numbers"
    #                     )
    #                     if len(st.session_state.selected_symbols) >= 2:
    #                         # show_stock_profile = st.sidebar.checkbox(
    #                         #     "Companies profile", value=False, key="show_stock_profile"
    #                         # )
    #                         show_correlation = st.sidebar.checkbox(
    #                             "Correlation", value=False, key="show_correlation"
    #                         )

    #         # (
    #         #     st.session_state.submit_button
    #         #     and len(st.session_state.selected_symbols) >= 1
    # ):
    #     show_stock_profile = st.sidebar.checkbox(
    #         "Companies profile", value=False, key="show_stock_profile"
    #     )
    # elif (
    #     st.session_state.submit_button
    #     and len(st.session_state.selected_symbols) >= 2
    # ):
    #     show_correlation = st.sidebar.checkbox(
    #         "Correlation", value=False, key="show_correlation"
    #     )

    # if (
    #     st.session_state.submit_button
    #     and len(st.session_state.selected_symbols) >= 1
    # ):
    #     show_mean = st.sidebar.checkbox("Mean", value=False, key="show_mean")

    # logic below for correlation calc and display
    if (
        st.session_state.selected_broker == "Alpha vantage_test"
        or st.session_state.selected_broker == "Twelve data"
    ):
        if len(st.session_state.selected_symbols) >= 1:
            # take the object  Dataframe_combine_builder from pipeline.multiple_dicts

            single_stock_prices = st.session_state.multi_builder.get_the_right_dict(
                "single_prices"
            )

            # Below for dev / debug purpose
            # print(type(stock_dict))
            # for key,value in stock_dict.items():
            #     print(f'key {key}, value : {value}')

            my_symbols = st.session_state.selected_symbols
            symbol_df_builder = multiple_data_frame.Dataframe_combine_builder()
            df_list = symbol_df_builder.list_merger(single_stock_prices, my_symbols)
            print(df_list)
            print("test")

            # merge those by columns
            if df_list:
                merged_lists = multiple_data_frame.Dataframe_combine_builder()
                st.session_state.merged_df_one = merged_lists.list_concacenate(df_list)
                st.dataframe(st.session_state.merged_df_one, width="stretch")
                print(st.session_state.merged_df_one)
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
                            "Companies profile", value=False, key="show_stock_profile"
                        )
                        show_basic_numbers = st.sidebar.checkbox(
                            "Basic numbers", value=False, key="show_basic_numbers"
                        )
                        if len(st.session_state.selected_symbols) >= 2:
                            # show_stock_profile = st.sidebar.checkbox(
                            #     "Companies profile", value=False, key="show_stock_profile"
                            # )
                            show_correlation = st.sidebar.checkbox(
                                "Correlation", value=False, key="show_correlation"
                            )


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


with tab3:
    if (
        st.session_state.selected_broker == "Alpha vantage_test"
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
                merged_df_array = numpy_calcs.Numpy_metrics_calcs.to_numpy(
                    st.session_state.merged_df_one
                )
                calc_array = numpy_calcs.Numpy_metrics_calcs(merged_df_array)

                for i, s in enumerate(st.session_state.selected_symbols):
                    with cols[i]:
                        # add here a function which will pull the start and end date frm the dataframe
                        st.markdown(f"### Stock symbol : {s}")

                        start_date = single_data_frame.Underlying_data_frame.first_date(
                            st.session_state.merged_df_one
                        )
                        end_date = single_data_frame.Underlying_data_frame.last_date(
                            st.session_state.merged_df_one
                        )

                        st.write(f"📅End date : {end_date} ")
                        st.write(f"📅Start date : {start_date} ")

                        last_price = calc_array.price_last(merged_df_array[:, i])
                        # st.write(f"Last price : {last_price}")
                        st.metric(label="Last close price", value=last_price)

                        price_min = calc_array.min_calc(merged_df_array[:, i])
                        # st.write(f"Min : {price_min}")
                        st.metric(label="Min", value=f"{price_min}")

                        price_max = calc_array.max_calc(merged_df_array[:, i])
                        # st.write(f"Max : {price_max}")
                        st.metric(label="Max", value=price_max)

                        price_mean = calc_array.mean_calc(merged_df_array[:, i])
                        # st.write(f"Mean : {price_mean}")
                        st.metric(label="Mean Price", value=price_mean)

                        mean_daily_return = calc_array.return_calcs_mean(
                            merged_df_array[:, i]
                        )
                        # st.write(f"Mean daily return(%): {mean_daily_return}")
                        st.metric(
                            label=f"Mean {price_type} return",
                            value=f"{mean_daily_return:.4f} %",
                        )

                        median_daily_return = calc_array.return_calcs_median(
                            merged_df_array[:, i]
                        )
                        # st.write(f"Mean daily return(%): {mean_daily_return}")
                        st.metric(
                            label=f"Median {price_type} return(%)",
                            value=median_daily_return,
                        )

                        return_min = calc_array.daily_return(merged_df_array[:, i])
                        return_min = calc_array.min_calc(return_min) * 100
                        # st.write(f"Min : {price_min}")
                        st.metric(
                            label=f"Min {price_type} return",
                            value=f"{return_min:.4f} %",
                        )

                        return_max = calc_array.daily_return(merged_df_array[:, i])
                        return_max = calc_array.max_calc(return_max) * 100
                        # st.write(f"Min : {price_min}")
                        st.metric(
                            label=f"Max {price_type} return",
                            value=f"{return_max:.4f} %",
                        )

                        return_st_dev = calc_array.st_dev_calc(merged_df_array[:, i])
                        return_st_dev = return_st_dev * 100
                        st.metric(
                            label=f"{price_type.capitalize()} standard deviation",
                            value=f"{return_st_dev:.4f} %",
                        )

                        cumulat_return = calc_array.cumulative_return(
                            merged_df_array[:, i]
                        )
                        # st.write(f"Cumulative return for given period : {cumulat_return} %")
                        st.metric(
                            label="Cumulative return for given period",
                            value=f"{cumulat_return} %",
                        )

            if st.session_state.show_stock_profile is True:
                single_company_info = st.session_state.finhub_info.get_the_right_dict(
                    "single_company_info"
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
                correlation_builder = correlation_helper(df_list)
                st.markdown("Calculated correlation is:")
                st.dataframe(correlation_builder, width="stretch")

        elif st.session_state.selected_broker == "Alpha vantage":
            if len(st.session_state.selected_symbols) >= 1:
                len_of_selected_symbols = len(st.session_state.selected_symbols)
            else:
                len_of_selected_symbols = 1
            cols = st.columns(len_of_selected_symbols)

            if len(st.session_state.selected_symbols) >= 1:

                if st.session_state.show_basic_numbers is True:

                    single_timeframe_returns = (
                        pipeline.multiple_dicts.get_the_right_dict(
                            "single_timeframe_returns"
                        )
                    )
                    timeframe_returns_dict = single_timeframe_returns.single_stock_data
                    print("dlugosc listy", len(timeframe_returns_dict))
                    for i in timeframe_returns_dict:
                        print(i)
                        print(type(i))

                    stock_dict = single_stock_prices.single_stock_data

                    # want to see for which symbols where the arrays built,
                    columns = st.session_state.merged_df_one.columns
                    merged_df_array = numpy_calcs.Numpy_metrics_calcs.to_numpy(
                        st.session_state.merged_df_one
                    )
                    calc_array = numpy_calcs.Numpy_metrics_calcs(merged_df_array)

                    for i, s in enumerate(st.session_state.selected_symbols):
                        with cols[i]:
                            # add here a function which will pull the start and end date frm the dataframe
                            st.markdown(f"### Stock symbol : {s}")

                            start_date = (
                                single_data_frame.Underlying_data_frame.first_date(
                                    st.session_state.merged_df_one
                                )
                            )
                            end_date = (
                                single_data_frame.Underlying_data_frame.last_date(
                                    st.session_state.merged_df_one
                                )
                            )

                            st.write(f"📅End date : {end_date} ")
                            st.write(f"📅Start date : {start_date} ")

                            last_price = calc_array.price_last(merged_df_array[:, i])
                            # st.write(f"Last price : {last_price}")
                            st.metric(label="Last close price", value=last_price)

                            price_min = calc_array.min_calc(merged_df_array[:, i])
                            # st.write(f"Min : {price_min}")
                            st.metric(label="Min", value=f"{price_min}")

                            price_max = calc_array.max_calc(merged_df_array[:, i])
                            # st.write(f"Max : {price_max}")
                            st.metric(label="Max", value=price_max)

                            price_mean = calc_array.mean_calc(merged_df_array[:, i])
                            # st.write(f"Mean : {price_mean}")
                            st.metric(label="Mean Price", value=price_mean)

                            mean_daily_return = calc_array.return_calcs_mean(
                                merged_df_array[:, i]
                            )
                            # st.write(f"Mean daily return(%): {mean_daily_return}")
                            st.metric(
                                label=f"Mean {price_type} return",
                                value=f"{mean_daily_return:.4f} %",
                            )

                            median_daily_return = calc_array.return_calcs_median(
                                merged_df_array[:, i]
                            )
                            # st.write(f"Mean daily return(%): {mean_daily_return}")
                            st.metric(
                                label=f"Median {price_type} return(%)",
                                value=median_daily_return,
                            )

                            return_min = calc_array.daily_return(merged_df_array[:, i])
                            return_min = calc_array.min_calc(return_min) * 100
                            # st.write(f"Min : {price_min}")
                            st.metric(
                                label=f"Min {price_type} return",
                                value=f"{return_min:.4f} %",
                            )

                            return_max = calc_array.daily_return(merged_df_array[:, i])
                            return_max = calc_array.max_calc(return_max) * 100
                            # st.write(f"Min : {price_min}")
                            st.metric(
                                label=f"Max {price_type} return",
                                value=f"{return_max:.4f} %",
                            )

                            return_st_dev = calc_array.st_dev_calc(
                                merged_df_array[:, i]
                            )
                            return_st_dev = return_st_dev * 100
                            st.metric(
                                label=f"{price_type.capitalize()} standard deviation",
                                value=f"{return_st_dev:.4f} %",
                            )

                            cumulat_return = calc_array.cumulative_return(
                                merged_df_array[:, i]
                            )
                            # st.write(f"Cumulative return for given period : {cumulat_return} %")
                            st.metric(
                                label="Cumulative return for given period",
                                value=f"{cumulat_return} %",
                            )

                if st.session_state.show_stock_profile is True:
                    for i, s in enumerate(st.session_state.selected_symbols):
                        with cols[i]:

                            single_company_info = (
                                st.session_state.finhub_info.get_the_right_dict(
                                    "single_company_info"
                                )
                            )
                            print(type(single_company_info))
                            print("SYBMOL", s)
                            single_profile = pipeline.single_company_info.get_the_right_first_level_dict(
                                s
                            )
                            st.dataframe(
                                {
                                    "Label": list(single_profile.keys()),
                                    "value": list(single_profile.values()),
                                },
                                hide_index=True,
                            )

            if st.session_state.show_correlation is True:
                # df_list = symbol_df_builder.list_merger(stock_dict, my_symbols) # seem to be not required
                # merge those by columns
                if df_list:
                    correlation_builder = correlation_helper(df_list)
                    st.markdown("Calculated correlation is:")
                    st.dataframe(correlation_builder, width="stretch")


with tab4:

    if st.session_state.submit_button:  # checking if submit button exists
        with st.sidebar:
            st.session_state.select_benchmarks = st.multiselect(
                "Select benchmarks",
                st.session_state.my_benchmarks,
                default=st.session_state.select_benchmarks,
                key="symbols_multiselect_benchmarks",
            )

    if (
        st.session_state.submit_button
        and len(st.session_state.selected_symbols) >= 1
        and len(st.session_state.select_benchmarks) >= 1
    ):
        with st.sidebar:
            st.title(":small[Benchmark metrics]")
            if (
                st.session_state.submit_button
                and len(st.session_state.selected_symbols) >= 1
            ):
                show_correlation_benchmark = st.sidebar.checkbox(
                    "Correlation", value=False, key="show_correlation_benchmark"
                )

    if st.session_state.show_correlation_benchmark is True:
        my_symbols_merged = combined_lists(
            st.session_state.select_benchmarks, st.session_state.selected_symbols
        )
        df_list_with_benchmark = symbol_df_builder.list_merger(
            single_stock_prices, my_symbols_merged
        )
        if df_list_with_benchmark:
            correlation_builder = correlation_helper(df_list_with_benchmark)
            st.markdown("Calculated correlation is:")
            st.dataframe(correlation_builder, width="stretch")
            with st.expander(" Pearson Correlation (r) definition, click to expand"):
                st.write(
                    """
                        What does it measure?
                        How strongly and linearly two instruments move together.
                        Range: from –1 to +1.

                        +1 → they move in the same direction, perfectly

                        0 → no linear relationship

                        –1 → they move in opposite directions

                        Most important: Correlation tells you only about the direction and consistency of movement, but not how many units something increases or decreases.

                        Example:
                        If the S&P 500 goes up by 1% → Apple often also goes up by around 1%
                        → high correlation (e.g., 0.9)
                        But we still don’t know whether Apple increases more or less.
                """
                )


# if st.session_state.submit_button and len(st.session_state.selected_symbols) >= 1:
#     show_worst_best = st.sidebar.checkbox("Worst and Best", value=False)
#     if show_worst_best is True:


# logic for Worst and Best Underlying


# adding some new  checklist button like "Visuals"
#   - normal price graphs
#   -


# https://docs.streamlit.io/develop/api-reference/text/st.markdown

# https://emojipedia.org/laptop
