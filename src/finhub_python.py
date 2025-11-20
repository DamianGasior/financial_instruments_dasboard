import finnhub
import pandas as pd

# https://github.com/Finnhub-Stock-API/finnhub-python

API_KEY = "d4ee4ppr01qrumpf24fgd4ee4ppr01qrumpf24g0"


# Setup client
finnhub_client = finnhub.Client(api_key=API_KEY)


class Finhub_data_builder:
    stock_companies_profile = {}
    dict_of_dict_finhub = {}

    @classmethod
    def get_company_info(cls, symbol):
        company_info = finnhub_client.company_profile2(symbol=symbol)  # symbol="AEM"
        # print(company_info)
        return company_info

        # method which will allow to add per symbol each received information to a dictionary

    @classmethod
    def add_stock_info(cls, symbol, passed_comp_info):
        cls.stock_companies_profile[symbol] = passed_comp_info
        return cls.stock_companies_profile

    @classmethod
    def add_dict_to_dict(
        cls, single_dict, name
    ):  # name to be like "single_company_info_"
        cls.dict_of_dict_finhub[name] = single_dict
        return cls.dict_of_dict_finhub

    @classmethod
    def get_the_right_first_level_dict(cls, symbol):
        value = cls.stock_companies_profile[symbol]
        print(value)
        return value

    @classmethod
    def get_the_right_dict(cls, name):
        specifc_dict_finhub = cls.dict_of_dict_finhub[name]
        print(specifc_dict_finhub)
        return specifc_dict_finhub

    @staticmethod
    def read_dict(passed_dict):
        for key, value in passed_dict.items():
            print(f"{key} : {value}")


# example_test = Finhub_data_builder.get_company_info("AEM")
# print(type(example_test))  # >> <class 'dict'>
# Finhub_data_builder.read_dict(example_test)


# single_stock = Finhub_data_builder.add_stock_info("AEM", example_test)
# print(type(single_stock))  # >> <class 'dict'>

# print("test")

# Finhub_data_builder.read_dict((Finhub_data_builder.stock_companies_profile))


# set_of_stocks = Finhub_data_builder.add_dict_to_dict(single_stock, "single_info")
# Finhub_data_builder.read_dict((Finhub_data_builder.dict_of_dict_finhub))


# reader_single_stock=single_stock.


# single_dict= Finhub_data_builder.add_stock_info(single_stock,'company_info')


# Company Profile
# print(finnhub_client.company_profile2(symbol='AAPL'))
# print(finnhub_client.company_profile(isin='US0378331005'))
# print(finnhub_client.company_profile(cusip='037833100'))

# # Financials as reported
# print(finnhub_client.financials_reported(symbol='AAPL', freq='annual'))


# Company News
# Need to use _from instead of from to avoid conflict
# print(finnhub_client.company_news('AAPL', _from="2025-11-01", to="2025-11-11"))


# print(finnhub_client.stock_insider_sentiment('AAPL', '2021-01-01', '2022-03-01'))


# print(finnhub_client.quote('AEM'))


# print(finnhub_client.company_basic_financials('AAPL', 'metric'))

# print(finnhub_client.symbol_lookup('AEM'))
# print(company_info)

# print("test_1")


# df = pd.DataFrame(company_info, index=[0])
# print(df)
# print("test_2")
# print(list(df.items()))

# # df = pd.DataFrame(list(df.items()), columns=["ticker", "price"])

# print("test AAPL")

# data = {"ticker1": ["AAPL"], "price1": [180], "ticker": ["MSFT"], "price": [200]}
# for key,value in data.items():
#     print(f'{key} : {value}')

# # data = [{"ticker1": "AAPL"}, {"price1": 180}, {"ticker": "MSFT", "price": 200}]
# # df1 = pd.DataFrame(data)

# # print(df1)


# data = {"ticker": ["AAPL", "MSFT"], "price": [180, 370]}
# df = pd.DataFrame(data)
# print(df)
