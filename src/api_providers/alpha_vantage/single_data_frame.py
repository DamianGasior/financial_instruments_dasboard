import pandas as pd
import streamlit as st
from src.pipeline.base_single_data_transformer import BaseDataTransformer

# from src.api_providers.alpha_vantage.api_request_alphavantage import (
#     Underlying_request_details,
# )


class Underlying_data_frame(BaseDataTransformer):
    def __init__(self, response_from_alpha):

        self.stock_symbol = Underlying_data_frame.import_symbol(response_from_alpha)
        print(self.stock_symbol)
        self.response_from_alpha = response_from_alpha
        self.close = self.stock_symbol
        # key_paremeter = Underlying_data_frame.search_key_param(response_from_alpha)
        price_adjustment = st.session_state.price_adjustment

        if price_adjustment == "non-adjusted":
            # key_paremeter = Underlying_data_frame.search_key_param(response_from_alpha)

            self.transform().set_date_as_index().column_rename(
                **{"1. open": "open"},
                **{"2. high": "high"},
                **{"3. low": "low"},
                **{"4. close": self.close},
                **{"5. volume": "volume"}
            )
        elif price_adjustment == "adjusted":
            # key_paremeter = Underlying_data_frame.search_key_param(response_from_alpha)
            self.transform().set_date_as_index().column_rename(
                **{"1. open": "open"},
                **{"2. high": "high"},
                **{"3. low": "low"},
                **{"5. adjusted close": self.close},
                **{"6. volume": "volume"}
            )
        self.leave_only_columns(
            self.close
        )  # in the future an option to the user can be enabled to choose from following columns ('open','high', 'low', 'close', 'volume')
        # self.add_new_columns()

    def search_key_param(api_response):
        list_of_params = [
            "Time Series (Daily)",
            "Weekly Time Series",
            "Monthly Time Series",
            "Weekly Adjusted Time Series",
            "Monthly Adjusted Time Series",
        ]
        for i in list_of_params:
            if i in api_response:
                return i

    def __getattr__(
        self, name
    ):  # dunder method, it allows to treat the class instance as dataframe
        return getattr(self.response_from_alpha, name)

    def transform(self):  # tu trzeba sie na tym skupic
        """based on the key_parameter we take from a set of dictionaries , the proper key = key_parameters;
            After the key is identified the Value is another set of dictionaries:
        The structure of self.response_from_alpha is as follows:
        {
            'Time Series (Daily)': {
                '2025-10-10': {
                    '1. open': '254.9400',
                    '2. high': '256.3800',
                    '3. low': '244.0000',
                    '4. close': '245.2700',
                    '5. volume': '61999098'
                },
                '2025-10-09': {
                    '1. open': '257.8050',
                    '2. high': '258.0000',
                    '3. low': '253.1400',
                    '4. close': '254.0400',
                    '5. volume': '38322012'
                },
                ...
            }...;
                  Since 'orient' is set to 'index', the outer dictionary keys (dates) become DataFrame rows (index).
        """
        self.response_from_alpha
        print(self.response_from_alpha)
        print("linia 88")
        key_paremeter = Underlying_data_frame.search_key_param(self.response_from_alpha)
        print("linia 73", self.response_from_alpha)
        print(key_paremeter)
        # once both borker will be using abstract class the below to be reviewed
        if key_paremeter is not None:
            required_data = self.response_from_alpha[key_paremeter]

            self.response_from_alpha = pd.DataFrame.from_dict(
                required_data, orient="index"
            )
            print("linia 77", self.response_from_alpha)
            return self
        elif key_paremeter is None:
            # df = self.response_from_alpha
            return self.response_from_alpha

    def set_date_as_index(self):
        self.response_from_alpha.index.name = (
            "Date"  # assiging the name of the columns as 'Date' which is our index
        )
        print("test", self.response_from_alpha)

        self.response_from_alpha.index = pd.to_datetime(
            self.response_from_alpha.index
        ).date  # .date function  is enough, no need for dt.date, as .date is typical for index
        # self.response_from_alpha.index=self.response_from_alpha.index.dt.date  <<this will not work
        # changing the columns ( apart of date one ) to int or float

        print("test2", self.response_from_alpha)

        for col in self.response_from_alpha:
            if not pd.api.types.is_datetime64_any_dtype(
                self.response_from_alpha[col]
            ):  # function is checking if each colums is not in a datetime format
                self.response_from_alpha[col] = pd.to_numeric(
                    self.response_from_alpha[col], errors="coerce"
                )  # applying the change, if not a number , then populate NaN
        return self

    def import_symbol(self):
        symbol = self["Meta Data"]["2. Symbol"]
        print(symbol)
        return symbol

    def leave_only_columns(self, *args):
        chosen_columns = []
        for column in args:
            chosen_columns.append(column)
        print(type(self))
        test = self.to_dataframe()
        print(test)
        self.response_from_alpha = test[chosen_columns]
        return self.response_from_alpha

    def __str__(self):
        return str(self.response_from_alpha.head(25))

    def show_columns(self):
        # print(f'type to: {type(self.response_from_alpha)}')
        print(self.response_from_alpha.dtypes)
        print(self.response_from_alpha.head())
        return self

    def column_rename(self, **kwargs):
        # columns #thnink if it should be alist or a dict or waht ?
        self.response_from_alpha.rename(columns=kwargs, inplace=True)
        return self

    def add_new_columns(self):
        self.response_from_alpha.insert(0, "symbol", self.stock_symbol)
        return self

    # this method helps to obtain by y any other requestor class the dataframe, when they will be hitting object_name.to_dataframe()
    def to_dataframe(self):
        return self.response_from_alpha

    @staticmethod
    def first_date(dataframe):
        oldest_date = dataframe.index.min()
        return oldest_date

    @staticmethod
    def last_date(dataframe):
        newest_date = dataframe.index.max()
        return newest_date

    # https://finnhub.io/docs/api/websocket-trades
