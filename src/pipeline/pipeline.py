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
from src.api_providers.finhub.finhub_python import Finhub_data_builder
from src.session_init import init_session_state


# multiple_data_frame = Dataframe_combine_builder()
# result_worst_and_best = Dataframe_combine_builder()
# corr_data_frame = Dataframe_combine_builder()
# multiple_dicts = Dataframe_combine_builder()
# single_company_info = Finhub_data_builder()
# dict_of_dift_finhub = Finhub_data_builder()


# class UnderlyingBuilder:
#     def __init__(
#         self,
#         underlying_reuqestor: Underlying_request_details,
#         df_builder_result: Dataframe_combine_builder | None = None,
#     ):
#         self.underlying_reuqestor = underlying_reuqestor
#         self.stock_symbol = underlying_reuqestor.symbol
#         self.key_paremeter = self.underlying_reuqestor.function
#         self.df_builder_result = df_builder_result

#     def run_pipeline(self):
#         if st.session_state.selected_broker == "Alpha vantage":
#             stock = self.underlying_reuqestor.api_request()
#             data_frame_builder = Underlying_data_frame(stock)
#             print('Type for  "data_frame_builder" is : ', type(data_frame_builder))
#             print(data_frame_builder)

#             # pdb.set_trace()
#             multiple_data_frame.add_to_dict(
#                 data_frame_builder, self.stock_symbol
#             )  #  adding to the  dict the df for price only
#             print(type(multiple_data_frame))
#             multiple_dicts.add_dict_to_dcit(
#                 multiple_data_frame, "single_prices"
#             )  #  creating a general df where the above iwll be added to an another df

#             # Type for  "data_frame_builder" is :  <class 'src.api_providers.alpha_vantage.single_data_frame.Underlying_data_frame'>
#             #                AEM
#             # 2025-12-08  164.72
#             print(self.underlying_reuqestor)

#             data_frame_builder_with_calcs = Underlying_metrics(
#                 self.underlying_reuqestor, data_frame_builder
#             )  # this was key , passing here the class parameters , and dataframe
#             print(data_frame_builder_with_calcs.price_chng_perct())
#             data_frame_builder_with_calcs

#             print(data_frame_builder_with_calcs.head())
#             print(type(data_frame_builder))
#             print(type(data_frame_builder_with_calcs))

#             # --- Preparing data and adding to dictionaries, which will be used to calculate correlation
#             data_frame_builder_corr = (
#                 data_frame_builder_with_calcs.copy_df()
#             )  # doing a copy in case I will work on 'data_frame_builder_corr'
#             # data_frame_builder_corr.copy_df()
#             print(data_frame_builder_corr.head())
#             print(type(data_frame_builder_corr))
#             corr_data_frame.add_to_dict(data_frame_builder_corr, self.stock_symbol)
#             multiple_dicts.add_dict_to_dcit(
#                 multiple_data_frame, "single_timeframe_returns"
#             )

#             # worst_and_best = data_frame_builder_with_calcs.worst_and_best()
#             # print(worst_and_best)
#             # print(type(worst_and_best))

#             request_company_info = Finhub_data_builder.get_company_info(
#                 self.stock_symbol
#             )

#             single_company_info.add_stock_info(self.stock_symbol, request_company_info)
#             # print(type(single_company_info))

#             dict_of_dift_finhub.add_dict_to_dict(
#                 single_company_info, "single_company_info"
#             )
#             # print(type(dict_of_dift_finhub))

#             # single_company_info = Finhub_data_builder.add_stock_info(
#             #     self.stock_symbol, request_company_info
#             # )
#             # dict_of_company_info = Finhub_data_builder.add_dict_to_dict(
#             #     single_company_info, "single_info"
#             # )

#         #         result_worst_and_best.add_to_list(worst_and_best)

#         #         stand_deviation_metrics=data_frame_builder_with_calcs.std_dev()
#         #         print(stand_deviation_metrics)

#     def run_merged_df_pipeline(self):
#         pass


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
