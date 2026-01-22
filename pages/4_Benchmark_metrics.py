import pdb
import streamlit as st
import sys  # allows to access to  information used by interpreter , in this case will be used to  point out to the src folder
import os  # allows to interact with the operating system , like checking the paths , catalogs and so on
import altair as alt
from streamlit_autorefresh import st_autorefresh
import numpy as np
from src.api_providers.common.multiple_data_frame import Dataframe_combine_builder

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
import pandas as pd
import logging

import plotly.express as px


from src.main import main

from src.pipeline import pipeline

# from src.pipeline.pipeline import DataPipeline
from src.api_providers.common import multiple_data_frame
from src.metrics import metrics_calcs
from src.metrics import numpy_calcs
from src.api_providers.alpha_vantage import single_data_frame

# from src.utils.main_utils import combined_lists
# from src.utils.streamlit_utils import correlation_helper, combined_lists
import altair as alt
from src.api_providers.finhub.finhub_python import Finhub_data_builder
from src.metrics.metrics_calcs import Underlying_metrics
from src.metrics import numpy_calcs
from src.session_init import init_session_state

init_session_state()

# st.write("PAGE:", __file__)  # this is for debugging purpose for dev work, shows the state of  all st.states
# st.write(st.session_state)   # this is for debugging purpose for dev work, shows the state of  all st.states


# from src.utils.streamalit_utlis import streamalit_utlis

# tab0,tab1,tab2,tab3
tab0, tab1 = st.tabs(
    [
        "SPY",
        "QQQ",
        # "EEM",
        # "GLD",
    ]
)


symbol_0 = "SPY"
symbol_1 = "QQQ"
symbol_2 = "EEM"
symbol_3 = "GLD"

symbol_df_builder = multiple_data_frame.Dataframe_combine_builder()
# list_of_benchmarks = [symbol_0, symbol_1, symbol_2, symbol_3]
list_of_benchmarks = [symbol_0, symbol_1]

# with tab0:

# df = pd.DataFrame {
#     "symbol" : pd.Series(dtype='str'),
#     "beta" : pd.Series(dtype='float'),
#     "std_devia" : pd.Series(dtype='float'),
#     "sharpe" : pd.Series(dtype='float'),
#     "alpha" : pd.Series(dtype='float'),
#     "r2" : pd.Series(dtype='float'),
#     "correlation": pd.Series(dtype='float'),
#     "corr_sign" : pd.Series(dtype='str')

# }

# if st.session_state.submit_button and len(st.session_state.selected_symbols) >= 1:

# my_symbols_merged = combined_lists(st.session_state.selected_symbols, symbol_0)
# print('my_symbols_merged',my_symbols_merged)
# print('st.session_state.selected_symbols',st.session_state.selected_symbols)

# df_list_with_benchmark = symbol_df_builder.list_merger(
#     st.session_state.single_stock_prices, my_symbols_merged
# )

# print('df_list_with_benchmark',df_list_with_benchmark)


beta_volatility = st.sidebar.checkbox(
    "Beta vs Volatility", value=False, key="Beta vs Volatility"
)


st.session_state.period_start_date = (
    multiple_data_frame.Dataframe_combine_builder.first_date(
        st.session_state.merged_df_one
    )
)
st.session_state.period_end_date = (
    multiple_data_frame.Dataframe_combine_builder.last_date(
        st.session_state.merged_df_one
    )
)

single_stock_prices = st.session_state.multi_builder.get_the_right_dict("single_prices")


# st.session_state.symbols_with_benchmark = (
#     numpy_calcs.DataFrameStore.new_list_with_benchmark(
#         st.session_state.selected_symbols, symbol_0
#     )
# )


if beta_volatility is True:

    with tab0:

        st.session_state.df_risk_info.beta_and_volatility_metrics(
            st.session_state.selected_symbols,
            symbol_0,
            single_stock_prices,
            list_of_benchmarks,
            st.session_state.users_price_type,
        )
        st.session_state.df_risk_info.show()
        plotly_df = st.session_state.df_risk_info.to_df()

        numpy_calcs.DataFrameStore.plotly_chart_beta_volatility(plotly_df, symbol_0)
        st.dataframe(
            st.session_state.df_risk_info.df
        )  # with the help of .df getting access to the class attribute
        numpy_calcs.DataFrameStore.beta_definition()

    with tab1:
        st.session_state.df_risk_info.beta_and_volatility_metrics(
            st.session_state.selected_symbols,
            symbol_1,
            single_stock_prices,
            list_of_benchmarks,
            st.session_state.users_price_type,
        )
        st.session_state.df_risk_info.show()
        plotly_df = st.session_state.df_risk_info.to_df()
        numpy_calcs.DataFrameStore.plotly_chart_beta_volatility(plotly_df, symbol_1)
        st.dataframe(st.session_state.df_risk_info.df)
        numpy_calcs.DataFrameStore.beta_definition()

    # with tab2:
    #     st.session_state.df_risk_info.beta_and_volatility_metrics(
    #         st.session_state.selected_symbols,
    #         symbol_2,
    #         single_stock_prices,
    #         list_of_benchmarks,
    #         st.session_state.users_price_type
    #     )
    #     st.session_state.df_risk_info.show()
    #     plotly_df = st.session_state.df_risk_info.to_df()
    #     numpy_calcs.DataFrameStore.plotly_chart_beta_volatility(plotly_df, symbol_2)
    #     st.dataframe(st.session_state.df_risk_info.df)
    #     numpy_calcs.DataFrameStore.beta_definition()

    # with tab3:
    #     st.session_state.df_risk_info.beta_and_volatility_metrics(
    #         st.session_state.selected_symbols,
    #         symbol_3,
    #         single_stock_prices,
    #         list_of_benchmarks,
    #         st.session_state.users_price_type
    #     )
    #     st.session_state.df_risk_info.show()
    #     plotly_df = st.session_state.df_risk_info.to_df()
    #     numpy_calcs.DataFrameStore.plotly_chart_beta_volatility(plotly_df, symbol_3)
    #     st.dataframe(st.session_state.df_risk_info.df)
    #     numpy_calcs.DataFrameStore.beta_definition()
