from src.api_providers.alpha_vantage.api_request_alphavantage import (
    Underlying_request_details,
)
from src.api_providers.twelve_data.to_dataframe_transofmer import (
    Underlying_twelve_data_details,
)
from src.api_providers.alpha_vantage.single_data_frame import Underlying_data_frame
from src.metrics.metrics_calcs import Underlying_metrics
from src.api_providers.common.multiple_data_frame import Dataframe_combine_builder
import pandas as pd
from src.api_providers.finhub.finhub_python import Finhub_data_builder
import streamlit as st
from src.pipeline.base_api_request import BaseAPIProvider
from src.pipeline.base_single_data_transformer import BaseDataTransformer
from typing import Optional
from src.session_init import init_session_state


class DataPipeline:

    transformer: BaseDataTransformer

    def __init__(
        self,
        provider: BaseAPIProvider,
        symbol,
        multi: Dataframe_combine_builder | None = None,
        metrics: Underlying_metrics | None = None,
        # finhub_info: Finhub_data_builder | None = None,
    ):
        self.provider = provider
        self.transformer = None
        self.symbol = symbol
        self.multi = multi
        self.metrics = metrics
        # self.finhub_info = finhub_info

    def run(self):
        init_session_state()
        api_request = self.provider.execute_full_request()
        self.transformer = self.provider.create_transformer(api_request)
        df_builder = self.transformer.transform()

        self.multi = self.multi or st.session_state.multi_builder
        self.multi.execute_operation(df_builder, self.symbol)

        self.metrics = self.metrics or st.session_state.metrics_instance
        self.metrics.underlying_request = api_request
        self.metrics.underlying_df = df_builder
        self.metrics.symbol = self.symbol
        self.metrics.execute_metrics()

        finhub_info = st.session_state.finhub_info
        finhub_info.execute_finhub(self.symbol)

        return self.multi, self.metrics
