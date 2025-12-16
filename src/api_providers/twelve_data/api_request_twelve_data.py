import requests
from collections import deque
import pandas as pd
from datetime import date
from pathlib import Path
import requests_cache
import logging
import streamlit as st
from src.api_providers.twelve_data.to_dataframe_transofmer import (
    Underlying_twelve_data_details
)
from src.api_providers.common import utils


# requests_cache.clear()
import sqlite3
import pickle
import os
from dotenv import load_dotenv  # module which allows to read .env file

from src.pipeline.base_api_request import BaseAPIProvider


API_KEY = "88b6ba35bcfc4bd3b70febcfe923cda6"


# https://api.twelvedata.com/time_series?apikey=88b6ba35bcfc4bd3b70febcfe923cda6&symbol=AAPL&interval=1day&format=JSON&outputsize=100&previous_close=true&dp=4

td_queue_of_requests = deque()


class Underlying_twelve_data_reuquest(BaseAPIProvider):

    def __init__(
        self,
        symbol,
        interval="1day",  # this needs to be driven bu the user as well( limit it only to 1day,1week,1 month)
        outputsize=2,
        dp=4,
        previous_close=True,
        adjust=False,  # this is driven already by the users input
        apikey=API_KEY,
    ):
        self.apikey = apikey
        self.symbol = symbol
        self.interval = interval
        self.output_size = outputsize
        self.decimal_places = dp
        self.previous_close = previous_close
        self.adjust = adjust

    def to_dict_params(self):
        return self.__dict__

    def api_request(self):
        parameters = self.to_dict_params()
        url = "https://api.twelvedata.com/time_series?"

        resp = requests.get(url, params=parameters)
        response = resp.json()
        print(response)
        return response

    # def attach_to_queue(response):
    #     td_queue_of_requests.append(response)

    def execute_full_request(self):
        response = self.api_request()
        print(response)
        td_queue_of_requests.append(response)
        return response

    def create_transformer(self,api_request):
        return Underlying_twelve_data_details(api_request)
    
    def cache_manager(self):
        return super().cache_manager()
    
    def read_all_keys_values_from_api(self):
        return super().read_all_keys_values_from_api()
    
    
    def check_for_caches(self):
        return super().check_for_caches()
    
    def read_caches(self):
        return super().read_caches()
    


    


    # def transform(self,response):
    #     transformer = Underlying_twelve_data_details(response)
    #     return transformer.transform()


# test_file = Underlying_twelve_data_reuquest(symbol="AAPL")
# # test_file.to_dict_params()
# test_file = test_file.api_request()
# print("test_file", type(test_file))


# transformed_test_file = Underlying_twelve_data_details(test_file)
# testing = transformed_test_file.transform()

# # transformed_test_file.show_columns(transformed_test_file)

# print(type(transformed_test_file))

# transformed_with_index = utils.set_date_as_index(testing)
# print(transformed_with_index)


# transformed_with_index = utils.column_rename(
#     transformed_with_index, **{"close": "AAPL"}
# )
# print(transformed_with_index)
# transformed_with_index = utils.leave_only_columns(transformed_with_index, "AAPL")
# print(transformed_with_index)
# #
# show_data=Underlying_twelve_data_details.show_columns(transformed_test_file)


# python -m src.api_providers.twelve_data.api_request_twelve_data
