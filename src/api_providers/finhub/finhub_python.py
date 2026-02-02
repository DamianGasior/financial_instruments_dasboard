import finnhub
import pandas as pd
import streamlit as st
import time
from datetime import datetime
from src.utils.streamlit_utils import key_validation
import os
from dotenv import load_dotenv
from pathlib import Path
import logging

# https://github.com/Finnhub-Stock-API/finnhub-python


FINHUB_KEY_PATH = Path(__file__).parent.parent.parent / "src" / ".env"
# load_dotenv(FINHUB_KEY_PATH)
# API_KEY = os.getenv("finhub_key")
key_name="finhub_key"

def api_key_request():
    API_KEY=key_validation(FINHUB_KEY_PATH,key_name)
    if API_KEY is None:
        API_KEY = key_validation(FINHUB_KEY_PATH, key_name)
    else : 
        API_KEY
    logging.info(f"api_key is :{API_KEY}")
    return API_KEY


# Setup client
# finnhub_client = finnhub.Client(api_key=API_KEY)


class Finhub_data_builder:

    # finnhub_client = finnhub.Client(api_key=API_KEY)

    def __init__(self):
        self.stock_companies_profile = {}
        self.dict_of_dict_finhub = {}
        self.last_close_prices = {}
        # self.symbol = symbol

    @classmethod
    @st.cache_data
    def get_company_info(cls, symbol):
        API_KEY=api_key_request()
        finnhub_client = finnhub.Client(api_key=API_KEY)
        
        company_info = finnhub_client.company_profile2(symbol=symbol)
        print("company_info", company_info)
        print('function fired,"time":,', datetime.now().isoformat())
        if company_info == {}:
            company_info = {symbol: "No data available"}

        return company_info

    def get_the_right_first_level_dict(self, symbol):
        value = self.stock_companies_profile[symbol]
        print(value)
        return value

    def get_the_right_dict(self, name):
        specifc_dict_finhub = self.dict_of_dict_finhub[name]
        print(specifc_dict_finhub)
        return specifc_dict_finhub

    
    def execute_finhub(self, symbol):
        stock_info = self.get_company_info(symbol)
        print(stock_info)
        if "single_company_info" not in self.dict_of_dict_finhub:
            self.dict_of_dict_finhub["single_company_info"] = {}
        self.dict_of_dict_finhub["single_company_info"][symbol] = stock_info
        print(
            'zawartosc - "single_company_info" ',
            self.dict_of_dict_finhub["single_company_info"].keys(),
            'zawartosc values  - "single_company_info" ',
            self.dict_of_dict_finhub["single_company_info"].values(),
        )

    # @st.cache_data
    def request_for_previous_close(self, *args):
        for selected_list in args:
            for symbol in selected_list:
                last_close_request = finnhub_client.quote(symbol)
                if last_close_request is not None:
                    close_price = last_close_request.get("pc")
                    print(last_close_request)
                    print(f"{symbol}-{close_price}")
                    self.last_close_prices[symbol] = close_price
        return self.last_close_prices

    @staticmethod
    def read_dict(passed_dict):
        for key, value in passed_dict.items():
            print(f"{key} : {value}")
