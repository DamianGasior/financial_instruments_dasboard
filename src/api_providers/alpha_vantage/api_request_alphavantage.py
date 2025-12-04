import requests
import time
import pandas as pd
from datetime import date
from pathlib import Path
import requests_cache
import logging
import streamlit as st

# requests_cache.clear()
import sqlite3
import pickle
import os
from dotenv import load_dotenv  # module which allows to read .env file

# Frist file for getting the data

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)


BASE_DIR = Path(__file__).resolve().parents[2]
#what does parents mean ? 
# Levels up
# parents[0] → alpha_vantage
# parents[1] → api_providers
# parents[2] → src ← here we want to get

load_dotenv(BASE_DIR / ".env")  # loads are variables from .env file and caches those
# load_dotenv(BASE_DIR / ".env_example")  # loads are variables from .env file and caches those
API_KEY = os.getenv(
    "apikey_alpha_vantage"
)  # use the variable loaded from the line above

# BASE_DIR_raw = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA = DATA_DIR / "raw"  # ...Python/financial_instruments_dasboard/src/data/raw
PROCESSED_DATA = DATA_DIR / "processed"


RAW_DATA.mkdir(parents=True, exist_ok=True)
PROCESSED_DATA.mkdir(parents=True, exist_ok=True)


class Underlying_request_details:
    cache_path = RAW_DATA / "alpha_cache"
    cache_path.parent.mkdir(parents=True, exist_ok=True)

    def __init__(self, symbol, function, outputsize, datatype, apikey=API_KEY):
        self.apikey = apikey
        self.symbol = symbol
        self.function = function
        self.outputsize = outputsize
        self.datatype = datatype
        self.cache_path = (
            Path(self.__class__.cache_path) / f"{symbol}"
        )  # using  class atrribute
        self.db_file = Path(self.cache_path).with_suffix(".sqlite")

    def cache_manager(self):

        requests_cache.install_cache(
            self.cache_path,
            backend="sqlite",
            expire_after=10000,
            allowable_methods=("GET", "POST"),
            serializer="pickle",
        )

    def to_dict_params(self):
        return self.__dict__

    def request_to_ext_api(self):
        self.cache_manager()
        params = self.to_dict_params()
        url = "https://www.alphavantage.co/query"
        try:
            resp = requests.get(url, params=params)
            resp.raise_for_status()
            logging.info(f"Response type is : {resp}")
            st.info(f"Response type is : {resp}")

        except requests.exceptions.Timeout:
            print("Error: Server did not respond.Try again later.")
            return "Error: Server did not respond.Try again later."
            # return None

        except requests.exceptions.HTTPError as e:
            print(f"Http error: {e}")
            return f"Http error: {e}"
            # return None

        except requests.exceptions.RequestException as e:
            print(f"Another error type: {e}")
            return f"Another error type: {e}"
            # return None

        if resp.status_code == 200 and "Information" in resp.json():
            timeout_message = resp.json()
            print(
                f"Limit API was reached, see comment : {timeout_message},wait 60 seconds please"
            )
            st.info(
                f"Limit API was reached, see comment : {timeout_message},wait 60 seconds please"
            )
            time.sleep(60)
            return (
                self.request_to_ext_api()
            )  # expose this in the streamlit UI in the main page
        elif resp.status_code == 200 and (getattr(resp, "from_cache", False)) is False:
            logging.info("response was succesfull (200)")
            st.success("response was succesfull (200)")
        elif getattr(resp, "from_cache", False) is True:
            logging.info("Response is from cache.")
            st.info("Response is from cache.")
        else:
            print(f"Response failed : {resp.status_code}")
            st.error(f"Response failed : {resp.status_code}")

        response = resp.json()
        print(response)

        # print(json.dumps(response,indent=4)) # to see what is the json format response
        return response

    def read_all_keys_values_from_api(self):
        # reads all the keys and values from request_to_ext_api() , from api or caches
        resp = self.request_to_ext_api()
        # resp=resp.json()
        for key, value in resp.items():
            print(f'KEY IS : {key}, ":", VALUE IS : {value} \n')

    def check_for_caches(self):
        # połączenie z bazą
        conn = sqlite3.connect(self.db_file)
        # lista tabel
        tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';", conn)
        print("Tabele w cache DB:\n", tables)
        if "responses" in tables["name"].values:
            df = pd.read_sql("SELECT * FROM responses", conn)
            print("Responses rows:", len(df))
        else:
            print("Brak tabeli responses (jeszcze nic nie zostało zapisane).")
        conn.close()

    def read_caches(self):
        print(self.db_file)
        conn = sqlite3.connect(self.db_file)
        df = pd.read_sql("SELECT * FROM responses", conn)
        print(df.columns.tolist())
        # Rozpakowujemy pierwszy rekord\

        raw_value2 = df.loc[0, "value"]
        resp_cached2 = pickle.loads(raw_value2)
        print(resp_cached2)

        # URL requesta
        print("URL:", resp_cached2["url"])

        # Dane JSON odpowiedzi

        conn.close()
