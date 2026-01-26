import streamlit as st
# from src.metrics.metrics_calcs import Underlying_metrics
# from src.metrics.numpy_calcs import DataFrameStore
# from src.api_providers.common.multiple_data_frame import Dataframe_combine_builder
# from src.api_providers.finhub.finhub_python import Finhub_data_builder

from src.metrics import metrics_calcs
from src.metrics import numpy_calcs
from src.api_providers.common import multiple_data_frame
from src.api_providers.finhub import finhub_python


def init_session_state():
    if "multi_builder" not in st.session_state:
        st.session_state.multi_builder = multiple_data_frame.Dataframe_combine_builder()

    if "metrics_instance" not in st.session_state:
        st.session_state.metrics_instance = metrics_calcs.Underlying_metrics()

    if "finhub_info" not in st.session_state:
        st.session_state.finhub_info = finhub_python.Finhub_data_builder()

    if "df_risk_info" not in st.session_state:
        st.session_state.df_risk_info = numpy_calcs.DataFrameStore()

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

    if "ui_selected_symbols" not in st.session_state:
        st.session_state.ui_selected_symbols = []

    if "select_benchmarks" not in st.session_state:
        st.session_state.select_benchmarks = []

    if "my_benchmarks" not in st.session_state:
        st.session_state.my_benchmarks = []

        # expand / add realtive_coparison
    if "symbols_for_my_list" not in st.session_state:
        st.session_state.symbols_for_my_list = []

    if "my_list" not in st.session_state:
        st.session_state.my_list = []
   
    if "my_list_info_for_user" not in st.session_state:
        st.session_state.my_list_info_for_user = None

    if "final_list" not in st.session_state:
        st.session_state.final_list = []

    if "show_correlation_benchmark" not in st.session_state:
        st.session_state.show_correlation_benchmark = False

    if "users_price_type" not in st.session_state:
        st.session_state.users_price_type = None
    
    if "success_symbols" not in st.session_state:
        st.session_state.success_symbols = []

    if "symbol_deque" not in st.session_state:
        st.session_state.symbol_deque = None
    
    if "autorefresh" not in st.session_state:
        st.session_state.autorefresh = False

    if "price_type" not in st.session_state:
        st.session_state.price_type = "TIME_SERIES_DAILY"

    if "price_adjustment" not in st.session_state:
        st.session_state.price_adjustment = "non-adjusted"

    if "selected_broker" not in st.session_state:
        st.session_state.selected_broker = None

    if "single_stock_prices" not in st.session_state:
        st.session_state.single_stock_prices = None

    if "my_merged_list" not in st.session_state:
        st.session_state.my_merged_list = []

    if "symbols_with_benchmark" not in st.session_state:
        st.session_state.symbols_with_benchmark = None

    if "period_start_date" not in st.session_state:
        st.session_state.period_start_date = None

    if "period_end_date" not in st.session_state:
        st.session_state.period_end_date = None

    if "correlation_benchmark" not in st.session_state:
        st.session_state.correlation_benchmark = False

    if "std_dev" not in st.session_state:
        st.session_state.std_dev = False

    if "beta_volatility" not in st.session_state:
        st.session_state.beta_volatility = False

    if "set_of_last_close_prices" not in st.session_state:
        st.session_state.set_of_last_close_prices = None
