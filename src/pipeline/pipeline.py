from src.api_providers.alpha_vantage.api_request_alphavantage import Underlying_request_details
from src.api_providers.alpha_vantage.single_data_frame import Underlying_data_frame
from src.metrics.metrics_calcs import Underlying_metrics
from src.api_providers.common.multiple_data_frame import Dataframe_combine_builder
import pandas as pd
from src.api_providers.finhub.finhub_python import Finhub_data_builder
import streamlit as st


multiple_data_frame = Dataframe_combine_builder()
result_worst_and_best = Dataframe_combine_builder()
corr_data_frame = Dataframe_combine_builder()
multiple_dicts = Dataframe_combine_builder()
single_company_info = Finhub_data_builder()
dict_of_dift_finhub = Finhub_data_builder()


class UnderlyingBuilder:
    def __init__(
        self,
        underlying_reuqestor: Underlying_request_details,
        df_builder_result: Dataframe_combine_builder | None = None,
    ):
        self.underlying_reuqestor = underlying_reuqestor
        self.stock_symbol = underlying_reuqestor.symbol

        if (
            self.underlying_reuqestor.function == "TIME_SERIES_DAILY"
            or self.underlying_reuqestor.function == "TIME_SERIES_DAILY_ADJUSTED"
        ):
            self.key_paremeter = "Time Series (Daily)"
            self.df_builder_result = df_builder_result
        elif self.underlying_reuqestor.function == "TIME_SERIES_WEEKLY":
            self.key_paremeter = "Weekly Time Series"
            self.df_builder_result = df_builder_result
        elif self.underlying_reuqestor.function == "TIME_SERIES_MONTHLY":
            self.key_paremeter = "Monthly Time Series"
            self.df_builder_result = df_builder_result
        elif self.underlying_reuqestor.function == "TIME_SERIES_WEEKLY_ADJUSTED":
            self.key_paremeter = "Weekly Adjusted Time Series"
            self.df_builder_result = df_builder_result
        elif self.underlying_reuqestor.function == "TIME_SERIES_MONTHLY_ADJUSTED":
            self.key_paremeter = "Monthly Adjusted Time Series"
            self.df_builder_result = df_builder_result

    def run_pipeline(self, underlying_reuqestor):
        if st.session_state.selected_broker == "Alpha vantage":
            stock = self.underlying_reuqestor.request_to_ext_api()
            data_frame_builder = Underlying_data_frame(
                stock,
                self.key_paremeter,
                underlying_reuqestor,
                st.session_state.price_adjustment,
            )
            print('Type for  "data_frame_builder" is : ', type(data_frame_builder))
            print(data_frame_builder)

            # pdb.set_trace()
            multiple_data_frame.add_to_dict(
                data_frame_builder, self.stock_symbol
            )  #  adding to the  dict the df for price only
            print(type(multiple_data_frame))
            multiple_dicts.add_dict_to_dcit(
                multiple_data_frame, "single_prices"
            )  #  creating a general df where the above iwll be added to an another df

            data_frame_builder_with_calcs = Underlying_metrics(
                self.underlying_reuqestor, data_frame_builder
            )  # this was key , passing here the class parameters , and dataframe
            print(data_frame_builder_with_calcs.price_chng_perct())
            data_frame_builder_with_calcs

            print(data_frame_builder_with_calcs.head())
            print(type(data_frame_builder))
            print(type(data_frame_builder_with_calcs))

            # --- Preparing data and adding to dictionaries, which will be used to calculate correlation
            data_frame_builder_corr = (
                data_frame_builder_with_calcs.copy_df()
            )  # doing a copy in case I will work on 'data_frame_builder_corr'
            # data_frame_builder_corr.copy_df()
            print(data_frame_builder_corr.head())
            print(type(data_frame_builder_corr))
            corr_data_frame.add_to_dict(data_frame_builder_corr, self.stock_symbol)
            multiple_dicts.add_dict_to_dcit(multiple_data_frame, "single_timeframe_returns")

            worst_and_best = data_frame_builder_with_calcs.worst_and_best()
            print(worst_and_best)
            print(type(worst_and_best))

            request_company_info = Finhub_data_builder.get_company_info(self.stock_symbol)

            single_company_info.add_stock_info(self.stock_symbol, request_company_info)
            # print(type(single_company_info))

            dict_of_dift_finhub.add_dict_to_dict(single_company_info, "single_company_info")
            # print(type(dict_of_dift_finhub))

            # single_company_info = Finhub_data_builder.add_stock_info(
            #     self.stock_symbol, request_company_info
            # )
            # dict_of_company_info = Finhub_data_builder.add_dict_to_dict(
            #     single_company_info, "single_info"
            # )

        #         result_worst_and_best.add_to_list(worst_and_best)

        #         stand_deviation_metrics=data_frame_builder_with_calcs.std_dev()
        #         print(stand_deviation_metrics)

    def run_merged_df_pipeline(self):
        pass


#         multiple_data_frame.multiple_data_frame_creator('multiples')
#         print(multiple_data_frame)
#         print(type(multiple_data_frame))

# # put later the results of this on a matplotlib ,  on x there will be months / days, on y will be the reurun
# result_worst_and_best.multiple_data_frame_creator('worst_and_best')
# print(result_worst_and_best)

# print(corr_data_frame.calc_correlation('correlation'))
