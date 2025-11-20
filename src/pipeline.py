from src.api_request_alphavantage import Underlying_request_details
from src.single_data_frame import Underlying_data_frame
from src.metrics_calcs import Underlying_metrics
from src.multiple_data_frame import Dataframe_combine_builder
import pandas as pd
from src.finhub_python import Finhub_data_builder


multiple_data_frame = Dataframe_combine_builder()
result_worst_and_best = Dataframe_combine_builder()
corr_data_frame = Dataframe_combine_builder()
multiple_dicts = Dataframe_combine_builder()
# single_data_frames=


class UnderlyingBuilder:
    def __init__(
        self,
        underlying_reuqestor: Underlying_request_details,
        df_builder_result: Dataframe_combine_builder | None = None,
    ):
        self.underlying_reuqestor = underlying_reuqestor
        self.stock_symbol = underlying_reuqestor.symbol

        if self.underlying_reuqestor.function == "TIME_SERIES_DAILY":
            self.key_paremeter = "Time Series (Daily)"
            #  will be expanded with other key.parametrs like for week and monthly
            self.df_builder_result = df_builder_result

    def run_pipeline(self, underlying_reuqestor):
        stock = self.underlying_reuqestor.request_to_ext_api()
        data_frame_builder = Underlying_data_frame(
            stock, self.key_paremeter, underlying_reuqestor
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
        single_company_info = Finhub_data_builder.add_stock_info(
            self.stock_symbol, request_company_info
        )
        dict_of_company_info = Finhub_data_builder.add_dict_to_dict(
            single_company_info, "single_info"
        )

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
