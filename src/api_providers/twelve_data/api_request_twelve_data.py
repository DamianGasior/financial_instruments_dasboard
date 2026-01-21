import requests
from collections import deque
import pandas as pd
from datetime import date
from pathlib import Path
import requests_cache
import logging
import streamlit as st
from src.api_providers.twelve_data.to_dataframe_transofmer import (
    Underlying_twelve_data_details,
)

# requests_cache.clear()
import sqlite3
import pickle
import os
from dotenv import load_dotenv  # module which allows to read .env file
from collections import defaultdict

from src.pipeline.base_api_request import BaseAPIProvider

TWELVEDATA_KEY_PATH = Path(__file__).parent.parent.parent / "src" / ".env"
load_dotenv(TWELVEDATA_KEY_PATH)
API_KEY = os.getenv("apikey_twelve_data")

# https://api.twelvedata.com/time_series?apikey=88b6ba35bcfc4bd3b70febcfe923cda6&symbol=AAPL&interval=1day&format=JSON&outputsize=100&previous_close=true&dp=4

td_queue_of_requests = deque()


class Underlying_twelve_data_reuquest(BaseAPIProvider):

    def __init__(
        self,
        symbol,
        adjust,  # this is driven already by the users input
        interval,  # this needs to be driven bu the user as well( limit it only to 1day,1week,1 month)
        outputsize=252,
        dp=4,
        previous_close=True,
        apikey=API_KEY,
    ):
        self.apikey = apikey
        self.symbol = symbol
        self.interval = interval
        self.outputsize = outputsize
        self.decimal_places = dp
        self.previous_close = previous_close
        self.adjust = adjust

    def to_dict_params(self):
        return self.__dict__

    # @st.cache_data(ttl=3600)  # ttl = time-to-live w sekundach
    def api_request(self):
        parameters = self.to_dict_params()
        url = "https://api.twelvedata.com/time_series?"
        try:
            resp = requests.get(url, params=parameters)
            print(type(resp))  # <class 'requests.models.Response'>
            response = resp.json()
            print(response)
            print(type(response))  # <class 'dict'>
            # if resp.status_code == 200
            code = response.get("code")
            message = response.get("message")

            logging.info(f"Response type is : {resp.status_code}")

            if resp.status_code == 200:
                # for success scenario
                if "meta" in resp.json():
                    logging.info(
                        f"Request was executed succefully for symbol: {self.symbol}"
                    )
                    symbol_received = response["meta"]["symbol"]
                    if symbol_received in st.session_state.my_benchmarks:
                        st.success(
                            # f"""Data received for symbol: {response["meta"]["symbol"]}"""
                            f"""Data received for bechmark symbol: {symbol_received}"""
                        )
                    else:
                        st.success(
                            # f"""Data received for symbol: {response["meta"]["symbol"]}"""
                            f"""Data received for symbol: {symbol_received}"""
                        )

                    return response
                # in case API will come back with an error
                elif "code" in response.keys():
                    logging.info(f"Response type is : {code}. Response is {message}")

                    # st.error(
                    #     f""""Resposne from broker : Error received with code: {code}.
                    #         Message: {response["message"]}"""
                    # )
                    raise Exception(
                        f'Broker error  {response.get("code")} : {response.get("message")}'
                    )  # passing this to UI , will be picked up as e
                # other unexpected cases
                else:
                    raise Exception(f"Unexpected response {response}")

        except requests.RequestException as e:
            raise Exception(
                f"Transport erorr{e}"
            )  # thanks to that we will get one f-string , ane
            # will be not getting this error :
            # TypeError: AlertMixin.error() takes 2 positional arguments but 3 were given
            # when it would implemented like this : st.error("Error occured", e)

    def execute_full_request(self):
        print("request_executed_by_twelve_data")
        response = self.api_request()
        print(response)
        td_queue_of_requests.append(response)
        return response

    def create_transformer(self, api_request):
        return Underlying_twelve_data_details(api_request)

    def cache_manager(self):
        return super().cache_manager()

    def read_all_keys_values_from_api(self):
        return super().read_all_keys_values_from_api()

    def check_for_caches(self):
        return super().check_for_caches()

    def read_caches(self):
        return super().read_caches()

    @staticmethod
    @st.cache_data(ttl=600)
    def symbol_search(users_input, apikey=API_KEY):

        initial_list = []
        dummy_list = []
        url = "https://api.twelvedata.com/symbol_search?symbol="
        request = url + users_input + "&outputsize=120" + "&" + apikey
        resp = requests.get(request)
        response = resp.json()
        print("raw_resposne:", response)
        print(type(response))  # <class 'dict'>
        # if resp.status_code == 200
        returned_data = response.get("data")

        for filtered_item in returned_data:
            if filtered_item.get("instrument_type") in [
                "Physical Currency",
                "Digital Currency",
            ]:
                initial_list.append(filtered_item)

        for filtered_item in returned_data:
            if filtered_item.get("country") in ["United States"]:
                initial_list.append(filtered_item)

        print("initial_list", initial_list)

        grouped = defaultdict(list)  # if there is no key, create an empty list

        for item in initial_list:
            grouped[item["instrument_type"]].append(item)

        grouped = dict(grouped)
        print(grouped)

        options = {}

        for group_name, value in grouped.items():
            for item in value:
                label = (
                    f"[{group_name}]"
                    f"{item['symbol']} - {item['instrument_name']}"
                    f"exchange : {item['exchange']}"
                )
                options[label] = item

        return options

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
