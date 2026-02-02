import pandas as pd
from datetime import date
from pathlib import Path
from dotenv import load_dotenv  # module which allows to read .env file

from src.api_providers.alpha_vantage.api_request_alphavantage import (
    Underlying_request_details,
)
from src.api_providers.alpha_vantage.single_data_frame import Underlying_data_frame


class Underlying_metrics:

    def __init__(
        self,
        underlying_request=None,
        underlying_df=None,
        symbol=None,
    ):
        # self.underlying_request=underlying_request
        # self.symbol = underlying_request.symbol
        self.symbol = symbol
        print(type(underlying_df))

        self.close_price_type = "close"
        # self.underlying_df = underlying_df.to_dataframe()
        self.underlying_df = underlying_df
        self.single_stock_data = {}
        self.dict_of_dict = {}

    @property
    def return_for_symbol(self):
        if self.symbol is None:
            return None
        return f"{self.symbol}_prct_return"

    # def __getattr__(
    #     self, name
    # ):  # dunder method, it allows to treat the class instance as dataframe
    #     return getattr(self.underlying_df, name)

    def copy_df(self):
        self.test = self.underlying_df.loc[
            :, [self.return_for_symbol]
        ].copy()  # becasue we use [self.return_for_symbol] instead of this self.return_for_symbol, the copy is created as a dataframe with the name columns instead of a heading.
        # additionaly , using copy() is safer becase you store this a seperate instance in memory
        # print(type(test))
        # print(test.head())
        # chosen_columns.append(self.return_for_symbol)
        # print(type(test))
        # test=test[chosen_columns]
        # print(test.head())
        self.test.rename(columns={self.return_for_symbol: self.symbol}, inplace=True)
        # print(test.head())
        return self.test

    def price_chng_perct(self):
        # return_for_symbol='daily_return_'+self.symbol

        self.underlying_df[self.return_for_symbol] = (
            self.underlying_df[self.symbol].pct_change() * 100
        ).round(4)
        self.underlying_df = self.underlying_df.dropna()
        print(self.underlying_df)
        return self.underlying_df

    def price_chng_perct_for_list(self):
        # return_for_symbol='daily_return_'+self.symbol

        self.underlying_df[self.return_for_symbol] = (
            self.underlying_df[self.symbol].pct_change() * 100
        ).round(4)
        self.underlying_df = self.underlying_df.dropna()
        print(self.underlying_df)
        return self.underlying_df

    def std_dev(self):
        # print('standard deviation')

        stand_dev = self.underlying_df[self.close].std()
        mean = self.underlying_df[self.close].mean()
        stand_pct = stand_dev / mean * 100
        start_date = self.underlying_df.index.min()
        end_date = self.underlying_df.index.max()
        print(f"Standard deviation for {self.symbol} is {stand_dev}")
        result_st_dev = pd.DataFrame(
            {
                "Start_date": [start_date],
                "End_date": [end_date],
                "Symbol": [self.symbol],
                "Std_dev": [stand_dev],
                "Std_pct": [stand_pct],
            }
        )
        return result_st_dev

    # this can be moved to some utils together with the same methods from mulitple_Data_frame file
    def add_dict_to_dict(self, name, symbol, value):
        if name not in self.dict_of_dict:
            self.dict_of_dict[name] = {}
        self.dict_of_dict[name][symbol] = value
        return self.dict_of_dict

    # this can be moved to some utils together with the same methods from mulitple_Data_frame file
    # tbc if it will work for self.single_stock_data={} and for  self.dict_of_dict={}
    def get_the_right_df(self, stock):
        value = self.single_stock_data[stock]
        print(value)
        return value

    # this can be moved to some utils together with the same methods from mulitple_Data_frame file

    def get_the_right_dict(self, name):
        # print("Klucze dostępne:", self.dict_of_dict.keys())
        # print("values dostępne:", self.dict_of_dict.values())
        # print("Szukany klucz name:", name)
        specifc_dict = self.dict_of_dict[name]
        # print(specifc_dict)
        # print(type(specifc_dict))
        # df = pd.DataFrame(specifc_dict)
        return specifc_dict

    def execute_metrics(self):
        print(self.symbol)
        if self.symbol is None:
            pass
        elif self.symbol is not None:
            price_returns = self.price_chng_perct()
        print(type(price_returns), self.symbol)
        if "single_timeframe_returns" not in self.dict_of_dict:
            self.dict_of_dict["single_timeframe_returns"] = {}

        self.dict_of_dict["single_timeframe_returns"][self.symbol] = price_returns
        print(
            'zawartosc - single_timeframe_returns" ',
            self.dict_of_dict["single_timeframe_returns"].keys(),
        )

    @staticmethod
    def calc_correlation(concac_df):
        print(concac_df)
        corr_result = concac_df.corr()
        return corr_result

    @staticmethod
    def price_chng_perct_for_list(stock_prices, list_of_symbols):
        dummy_list = []

        for sel_symbol in list_of_symbols:
            dummy_df = pd.DataFrame()
            dummy_df = dummy_df.copy()
            asset_price = stock_prices.get(sel_symbol)
            print(asset_price)
            dummy_df.index = asset_price.index
            print(dummy_df.index)
            dummy_df[sel_symbol] = asset_price[sel_symbol].pct_change().dropna()

            print(dummy_df)
            dummy_df.dropna(inplace=True)
            print(dummy_df)
            dummy_list.append(dummy_df)

        print(len(dummy_list))
        return dummy_list
