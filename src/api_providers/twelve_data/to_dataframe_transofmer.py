import pandas as pd


class Underlying_twelve_data_details:
    def __init__(self, response_from_api):
        self.response_from_api = response_from_api

    def transform(self, key_paremeter="values", orient="index"):
        transformed_df=self.response_from_api[key_paremeter] # we take  from the dict received "values" as a key, so now we get a list of dict
        #raw json recieved 
        
        #input
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
        #output 
#[{'datetime': '2025-12-02', 'open': '283', 'high': '287.39999', 'low': '282.63010', 'close': '286.19000', 'volume': '47782384', 'previous_close': '283.10001'}, 
# {'datetime': '2025-12-01', 'open': '278.010010', 'high': '283.42001', 'low': '276.14001', 'close': '283.10001', 'volume': '46587700', 'previous_close': '278.85001'}
        df = pd.DataFrame(transformed_df) # above list of dicts is transformed to 
        print(type(df))
        print(df)

        return df
    


    # metode gdzie data  juet ustawiana jako index 
    
    @staticmethod
    def show_columns(df):
        # print(f'type to: {type(self.response_from_alpha)}')
        print(df)
        print(df.head())
        return df