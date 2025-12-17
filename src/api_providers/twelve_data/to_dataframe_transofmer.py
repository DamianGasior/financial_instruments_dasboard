import pandas as pd
from src.pipeline.base_single_data_transformer import BaseDataTransformer
from src.api_providers.common import utils

# from src.main import symbol


class Underlying_twelve_data_details(BaseDataTransformer):
    def __init__(self, response_from_api):
        self.response_from_api = response_from_api
        # self.symbol=symbol

    def transform(self, key_paremeter="values", orient="index"):
        transformed_df = self.response_from_api[
            key_paremeter
        ]  # we take  from the dict received "values" as a key, so now we get a list of dict
        # raw json recieved

        # input
        """{
    "meta": {
        "symbol": "AAPL",
        "interval": "1day",
        "currency": "USD",
        "exchange_timezone": "America/New_York",
        "exchange": "NASDAQ",
        "mic_code": "XNGS",
        "type": "Common Stock"
    },
    "values": [
        {
            "datetime": "2025-12-02",
            "open": "283",
            "high": "287.39999",
            "low": "282.655",
            "close": "286.23001",
            "volume": "38056166",
            "previous_close": "283.10001"
        },
        {
            "datetime": "2025-12-01",
            "open": "278.010010",
            "high": "283.42001",
            "low": "276.14001",
            "close": "283.10001",
            "volume": "46528400",
            "previous_close": "278.85001"
        },
"""
        # output
        # [{'datetime': '2025-12-02', 'open': '283', 'high': '287.39999', 'low': '282.63010', 'close': '286.19000', 'volume': '47782384', 'previous_close': '283.10001'},
        # {'datetime': '2025-12-01', 'open': '278.010010', 'high': '283.42001', 'low': '276.14001', 'close': '283.10001', 'volume': '46587700', 'previous_close': '278.85001'}
        df = pd.DataFrame(transformed_df)  # above list of dicts is transformed to
        print(type(df))
        print(df)
        symbol = Underlying_twelve_data_details.import_symbol(self.response_from_api)
        df = Underlying_twelve_data_details.set_date_as_index(df)
        df = Underlying_twelve_data_details.column_rename(df, **{"close": symbol})
        print(df)
        df = Underlying_twelve_data_details.leave_only_columns(df, symbol)
        print(df)
        self.symbol = Underlying_twelve_data_details.import_symbol(
            self.response_from_api
        )
        # df = utils.set_date_as_index(df)
        # df = utils.column_rename(df, **{"close": self.symbol})
        # print(df)
        # df = utils.leave_only_columns(df, self.symbol)
        # print(df)
        return df

    # metode gdzie data  juet ustawiana jako index

    def import_symbol(self):
        symbol = self["meta"]["symbol"]
        print(symbol)
        return symbol

    def search_key_param(api_response):
        return super().search_key_param()

    def set_date_as_index(df_from_api_provider):
        print("test", df_from_api_provider)
        # df_from_api_provider.index.name = (
        #     "Date"  # assiging the name of the columns as 'Date' which is our index
        # )
        df_from_api_provider = df_from_api_provider.set_index("datetime")
        print("test1", df_from_api_provider)
        df_from_api_provider.index.name = (
            "Date"  # changine the name of index column to "Date"
        )
        print("test2", df_from_api_provider)

        df_from_api_provider.index = pd.to_datetime(df_from_api_provider.index).date
        print("test3", df_from_api_provider)
        # self.response_from_alpha.index=self.response_from_alpha.index.dt.date  <<this will not work
        # changing the columns ( apart of date one ) to int or float
        for col in df_from_api_provider:
            if not pd.api.types.is_datetime64_any_dtype(
                df_from_api_provider[col]
            ):  # function is checking if each colums is not in a datetime format, if its not, then :
                df_from_api_provider[col] = pd.to_numeric(
                    df_from_api_provider[col], errors="coerce"
                )  # applying the change and convert to a number , "coerce"  means if the value can not be changed to number, convert to NaN
        return df_from_api_provider

    def column_rename(df_from_api_provider, **kwargs):
        # columns #thnink if it should be alist or a dict or waht ?
        df_from_api_provider.rename(columns=kwargs, inplace=True)
        return df_from_api_provider

    def leave_only_columns(df_from_api_provider, *args):
        chosen_columns = []
        for column in args:
            chosen_columns.append(column)
        df_from_api_provider = df_from_api_provider[chosen_columns]
        print(df_from_api_provider)
        return df_from_api_provider
    
    def to_dataframe(self):
        return super().to_dataframe()

    @staticmethod
    def show_columns(df):
        # print(f'type to: {type(self.response_from_alpha)}')
        print(df)
        print(df.head())
        return df
