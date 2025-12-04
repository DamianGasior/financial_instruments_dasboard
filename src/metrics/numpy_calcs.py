import numpy as np
import pandas as pd
from src.api_providers.alpha_vantage.single_data_frame import Underlying_data_frame

from src.api_providers.alpha_vantage.api_request_alphavantage import Underlying_request_details
from src.main import main
from src.pipeline import pipeline
from src.api_providers.common import multiple_data_frame
from src.metrics import metrics_calcs
from src.api_providers.alpha_vantage import single_data_frame


class Numpy_metrics_calcs:
    def __init__(self, incoming_dataframe):
        self.incoming_datafame = incoming_dataframe

    # Metrics are pure functions that operate on external NumPy arrays.
    # Using @classmethod allows calling them directly on the class without
    # instantiating objects and keeps the API clean and functional.

    @classmethod
    def to_numpy(cls, incoming_dataframe):
        array = incoming_dataframe.to_numpy()
        return array

    @classmethod
    def price_last(cls, array):
        price = array[0]
        return price

    @classmethod
    def mean_calc(cls, array):
        mean = np.round(array.mean(), 4)
        return mean

    @classmethod
    def median_calc(cls, array):
        median = np.round(array.median(), 4)
        return median

    @classmethod
    def min_calc(cls, array):
        mins = np.round(array.min(), 4)
        return mins

    @classmethod
    def max_calc(cls, array):
        mins = np.round(array.max(), 4)
        return mins

    @classmethod
    def return_calcs_mean(cls, array):
        daily_returns = Numpy_metrics_calcs.daily_return(array)
        mean_daily_return = np.round((np.mean(daily_returns) * 100), 4)
        return mean_daily_return

    @classmethod
    def return_calcs_median(cls, array):
        daily_returns = Numpy_metrics_calcs.daily_return(array)
        median_daily_return = np.round(np.median(daily_returns) * 100, 4)
        return median_daily_return

    @classmethod
    def cumulative_return(cls, array):
        cumulat_return = np.round(((array[0] / array[-1]) - 1) * 100, 4)
        return cumulat_return

    @classmethod
    def st_dev_calc(cls, array):
        daily_returns = Numpy_metrics_calcs.daily_return(array)
        st_dev_result = np.std(
            daily_returns, ddof=1
        )  # sample of data will be provided,  hence applying 1 instead of 0
        return st_dev_result

    @staticmethod
    def daily_return(array):
        daily_returns = np.diff(array) / array[:-1]
        print(f"test:{type(daily_returns)}")
        print(f"test2:{daily_returns.dtype}")
        return daily_returns
