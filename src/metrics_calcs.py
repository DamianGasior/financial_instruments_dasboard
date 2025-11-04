import pandas as pd
from datetime import date
from pathlib import Path
from dotenv import load_dotenv  # module which allows to read .env file

from src.api_request_alphavantage import Underlying_request_details
from src.single_data_frame import Underlying_data_frame


class Underlying_metrics:

    def __init__(
        self,
        underlying_request: Underlying_request_details | None = None,
        underlying_df: Underlying_data_frame | None = None,
        example_df: Underlying_data_frame | None = None,
    ):
        # self.underlying_request=underlying_request
        self.symbol = underlying_request.symbol
        self.return_for_symbol = self.symbol + "_prct_return"
        self.close = self.symbol
        self.underlying_df = underlying_df.to_dataframe()

    def __getattr__(
        self, name
    ):  # dunder method, it allows to treat the class instance as dataframe
        return getattr(self.underlying_df, name)

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
        # print( self.return_for_symbol)
        self.underlying_df[self.return_for_symbol] = (
            self.underlying_df[self.close].pct_change() * 100
        ).round(4)

        return self.underlying_df

    def worst_and_best(self):

        # row with the worst ( min) and the best (max)  performance, change percantage on the day
        worst_idx = self.underlying_df[self.return_for_symbol].idxmin()
        best_idx = self.underlying_df[self.return_for_symbol].idxmax()

        # values for the row above with the actual numbers from column 'return', with the help of .loc ( locator?)I can get with the help of label for column and row
        worst_val = self.underlying_df.loc[worst_idx, self.return_for_symbol]
        best_val = self.underlying_df.loc[best_idx, self.return_for_symbol]

        # the same as worst_idx and   best_idx , just assiging to variable with date
        worst_date = worst_idx
        best_date = best_idx

        # price level for that specifc day, the best and the worst day
        close_price_on_worst = self.underlying_df.loc[worst_idx, self.close]
        close_price_on_best = self.underlying_df.loc[best_idx, self.close]

        stocks = self.symbol

        result_df = pd.DataFrame(
            {
                "Date": [worst_date, best_date],
                # 'Symbol':[stocks,stocks],
                self.close: [close_price_on_worst, close_price_on_best],
                "Type": ["Worst", "Best"],
                "Return": [worst_val, best_val],
            }
        )

        return result_df

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

    # add average price, high and low for a sepcifc period, and the price for start date and end date.

    # think somehting about Volume, and what does it mean ...

    def calc_correlation(self):
        self = self.corr()
        return self
