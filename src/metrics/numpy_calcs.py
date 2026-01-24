import numpy as np
import pandas as pd
from src.api_providers.alpha_vantage.single_data_frame import Underlying_data_frame
import streamlit as st
from src.api_providers.alpha_vantage.api_request_alphavantage import (
    Underlying_request_details,
)
from src.api_providers.common import multiple_data_frame
from src.metrics import metrics_calcs
from src.api_providers.alpha_vantage import single_data_frame
import plotly.express as px
import logging
import plotly.graph_objects as go

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)


data_metrics = metrics_calcs.Underlying_metrics()

single_stock_prices = multiple_data_frame.Dataframe_combine_builder()

symbol_df_builder = multiple_data_frame.Dataframe_combine_builder()


class Numpy_metrics_calcs:
    def __init__(self, incoming_dataframe):
        self.incoming_datafame = incoming_dataframe

    # Metrics are pure functions that operate on external NumPy arrays.
    # Using @classmethod allows calling them directly on the class without
    # instantiating objects and keeps the API clean and functional.

    @staticmethod
    def to_numpy(incoming_dataframe):
        # print("incoming_dataframe")
        # print(incoming_dataframe)
        # print(incoming_dataframe.dtypes)
        # print(incoming_dataframe.columns)
        # print(incoming_dataframe.index)
        # print(incoming_dataframe.index.name)
        # print("last")
        # print(incoming_dataframe.info)
        incoming_dataframe_sorted = incoming_dataframe.sort_values("Date")
        price_array = incoming_dataframe_sorted.to_numpy()
        dates_price_array = incoming_dataframe_sorted.index.to_numpy()
        # print(price_array)
        # print(dates_price_array)
        return price_array, dates_price_array

    @classmethod
    def price_last(cls, array):
        price = array[-1]
        return price

    @classmethod
    def price_first(cls, array):
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
        mean_daily_return = np.round((np.mean(daily_returns)), 4)
        return mean_daily_return

    @classmethod
    def return_calcs_median(cls, array):
        daily_returns = Numpy_metrics_calcs.daily_return(array)
        median_daily_return = np.round(np.median(daily_returns), 4)
        return median_daily_return

    @classmethod
    def cumulative_return(cls, array):
        cumulat_return = np.round(((array[-1] / array[0]) - 1), 4)
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
        print(array)
        # tu trzeba zmienic tez
        daily_returns = np.diff(array) / array[:-1]
        print(f"test:{type(daily_returns)}")
        print(f"test2:{daily_returns.dtype}")
        print(daily_returns)
        return daily_returns


class DataFrameStore:
    def __init__(self, df: pd.DataFrame | None = None):
        # wewnętrzny DataFrame
        self.df = df if df is not None else pd.DataFrame()

    def to_df(self) -> pd.DataFrame:
        return self.df

    def append(self, new_df: pd.DataFrame):
        self.df = pd.concat([self.df, new_df])
        self.df = self.df.groupby("symbol", as_index=False).last()
        return self.df

        # self=self['symbol'].map(new_df)

    def show(self):
        print(self.df)

    def add_symbols(self, *args):
        for selected_list in args:
            for symbol in selected_list:
                self.append(pd.DataFrame([{"symbol": symbol}]))
        return self

    def beta_calcs(self, *args, benchmark, single_stock_prices):
        single_stock_prices = single_stock_prices
        print(single_stock_prices)
        benchmark_price = single_stock_prices.get(benchmark)
        if not benchmark_price.empty:
            logging.info(benchmark_price.to_string())
            logging.info(f"number of rows for {benchmark} is {len(benchmark_price)}")

        for selected_list in args:
            for symbol in selected_list:
                asset_price = single_stock_prices.get(symbol)
                if not asset_price.empty:
                    logging.info(asset_price.to_string())
                    logging.info(f"number of rows for {symbol} is {len(asset_price)}")

                benchmark_price_cut, asset_price_cut = (
                    multiple_data_frame.Dataframe_combine_builder.date_index_verfication(
                        benchmark_price, asset_price
                    )
                )

                asset_return = self.daily_return_array_helper(asset_price_cut)
                market_return = self.daily_return_array_helper(benchmark_price_cut)

                cov = np.cov(asset_return, market_return, ddof=1)[0, 1]
                print(cov)
                var = np.var(market_return, ddof=1)
                print(var)
                beta = cov / var
                print(beta)
                self.append(pd.DataFrame([{"symbol": symbol, "beta": beta}]))
        return self.df

    # the below does calculate only the correaltion between benchmark and single equity
    def correlation_calcs(self, *args, benchmark, single_stock_prices):

        single_stock_prices = single_stock_prices
        print(single_stock_prices)
        benchmark_price = single_stock_prices.get(benchmark)
        if not benchmark_price.empty:
            logging.info(benchmark_price.to_string())
            logging.info(f"number of rows for {benchmark} is {len(benchmark_price)}")

        for selected_list in args:
            for symbol in selected_list:
                asset_price = single_stock_prices.get(symbol)
                if not asset_price.empty:
                    logging.info(asset_price.to_string())
                    logging.info(f"number of rows for {symbol} is {len(asset_price)}")

                benchmark_price_cut, asset_price_cut = (
                    multiple_data_frame.Dataframe_combine_builder.date_index_verfication(
                        benchmark_price, asset_price
                    )
                )

                asset_return = self.daily_return_array_helper(asset_price_cut)

                market_return = self.daily_return_array_helper(benchmark_price_cut)

                corr_stock_benchmark = np.corrcoef(asset_return, market_return)[0, 1]
                print(corr_stock_benchmark)

                self.append(
                    pd.DataFrame(
                        [{"symbol": symbol, "correlation": corr_stock_benchmark}]
                    )
                )

        return self.df

    def r2_calc(self, *args):
        for selected_list in args:
            for symbol in selected_list:
                corr_value = self.df.loc[
                    self.df["symbol"] == symbol, "correlation"
                ].iloc[0]
                print(corr_value)
                r2 = corr_value**2
                self.append(pd.DataFrame([{"symbol": symbol, "R2": r2}]))
        return self.df

    def daily_return_array_helper(self, price_array):
        asset_price_array, dates_array = Numpy_metrics_calcs.to_numpy(price_array)
        asset_price_array = asset_price_array.flatten()
        asset_price_return = Numpy_metrics_calcs.daily_return(asset_price_array)
        asset_return_ndarray = (
            asset_price_return.ravel()
        )  # to get 1D vector instead of a matrix
        return asset_return_ndarray

    def std_dev_to_df(self, *args, single_stock_prices):
        for selected_list in args:
            for symbol in selected_list:
                asset_price = single_stock_prices.get(symbol)
                asset_price_array, dates_array = Numpy_metrics_calcs.to_numpy(
                    asset_price
                )
                asset_price_array = asset_price_array.ravel()
                std_d = Numpy_metrics_calcs.st_dev_calc(asset_price_array)
                std_d = round(std_d, 4)
                print(f"std_d for {symbol} is {std_d}")
                self.append(pd.DataFrame([{"symbol": symbol, "std_dev": std_d}]))
        return self.df

    def sharpe_ratio_calc(self, *args, period, single_stock_prices):
        rf_annual = 0.035
        if period == "weekly":
            rf_period = (1 + rf_annual) ** (1 / 52) - 1
        elif period == "monthly":
            rf_period = (1 + rf_annual) ** (1 / 12) - 1
        elif period == "daily":
            rf_period = (1 + rf_annual) ** (1 / 252) - 1
        else:
            rf_annual
        for selected_list in args:
            for symbol in selected_list:

                # array_transformed = array[:, i]
                asset_price = single_stock_prices.get(symbol)
                asset_price_array, dates_array = Numpy_metrics_calcs.to_numpy(
                    asset_price
                )
                asset_price_array = asset_price_array.ravel()
                mean_return = Numpy_metrics_calcs.return_calcs_mean(asset_price_array)
                mean_std_dev = Numpy_metrics_calcs.st_dev_calc(asset_price_array)
                sharpe_ratio = (mean_return - rf_period) / mean_std_dev
                print(f"sharpe_ratio {symbol} is {sharpe_ratio}")
                self.append(
                    pd.DataFrame([{"symbol": symbol, "sharpe_ratio": sharpe_ratio}])
                )
        return self.df
        # dostaje daily returns i licze ich mean
        # dostaje standardowe odchylenie zwrotu i licze


    # method which  will serve as a pipeline
    def beta_and_volatility_metrics(
        self, sel_symbols, benchmark, stock_prices, list_of_benchmarks, period
    ):
        self.add_symbols(sel_symbols, list_of_benchmarks)

        self.beta_calcs(
            sel_symbols,
            list_of_benchmarks,
            benchmark=benchmark,
            single_stock_prices=stock_prices,
        )

        self.std_dev_to_df(
            sel_symbols, list_of_benchmarks, single_stock_prices=stock_prices
        )
        self.sharpe_ratio_calc(
            list_of_benchmarks,
            sel_symbols,
            period=period,
            single_stock_prices=stock_prices,
        )

        self.correlation_calcs(
            sel_symbols,
            list_of_benchmarks,
            benchmark=benchmark,
            single_stock_prices=stock_prices,
        )

        self.r2_calc(sel_symbols, list_of_benchmarks)

        return self.df

    @staticmethod
    def plotly_chart_beta_volatility(incoming_dataframe, benchmark):
        incoming_dataframe["R2_size"] = incoming_dataframe["R2"] ** 0.2

        fig = px.scatter(
            incoming_dataframe[incoming_dataframe["symbol"] != benchmark],
            x="beta",
            y="std_dev",
            text="symbol",
            hover_name="symbol",
            hover_data={
                "beta": ":.2f",
                "std_dev": ":.2f",
                "R2": ":.2f",
            },
            color="sharpe_ratio",
            size="R2_size",
            size_max=25,
            color_continuous_scale=[
                (0.0, "darkred"),
                (0.45, "orangered"),
                (0.50, "lightgray"),  # Sharpe ≈ 0
                (0.55, "limegreen"),
                (1.0, "darkgreen"),
            ],
            color_continuous_midpoint=0,
            title=(
                f"Risk Map: Beta vs Volatility<br>"
                f"Benchmark: {benchmark}<br> "
                f"Period: {st.session_state.period_start_date} – "
                f"{st.session_state.period_end_date}"
            ),
        )

        # benchmark jako osobny trace
        benchmark_df = incoming_dataframe[incoming_dataframe["symbol"] == benchmark]

        fig.add_trace(
            go.Scatter(
                x=benchmark_df["beta"],
                y=benchmark_df["std_dev"],
                mode="markers+text",
                text=[benchmark],
                textposition="top right",
                marker=dict(size=18, symbol="star", color="green"),
                # name=f"{benchmark} (Benchmark)",
            )
        )

        fig.update_traces(textposition="top center", marker=dict(size=10))

        fig.add_vline(x=1, line_dash="dash", line_color="black")
        fig.add_hline(
            y=benchmark_df["std_dev"].iloc[0], line_dash="dash", line_color="black"
        )

        st.plotly_chart(fig, use_container_width=True)

    @staticmethod
    def beta_definition():
        with st.expander("One liner metric explanation, click to expand"):
            st.write(
                f"""

X = Beta → „Shows how strongly the stock moves compared to the market.”

Y = Std Dev (Volatility) → „Shows how much the stock’s price swings overall.”

Color = Sharpe Ratio → „Shows how good the stock’s return is relative to the risk it takes against risk free rate, set at 3.5 %”

Size = R² → „Shows how much of the stock’s movement is explained by the market.”
"""
            )

        with st.expander("Beta  and standard deviation(volatility) definitions, click to expand"):
            st.write(
                """
Beta – "how much a stock moves RELATIVE to the market"

Definition:
Beta indicates how strongly and in which direction a stock’s return responds to changes in the market (benchmark).

Interpreting Beta values:

Beta	Practical meaning
β = 1.0	The stock moves in line with the market

β > 1.0	More aggressive than the market

0 < β < 1	Defensive / less sensitive than the market

β = 0	No correlation with the market

β < 0	Moves opposite to the market (rare)

📌 Example:

β = 1.5 → when the market rises by +1%, the stock typically rises by +1.5%

β = 0.6 → when the market falls by -1%, the stock falls by only -0.6%

👉 Beta = systematic risk (cannot be diversified away).

Standard Deviation of Returns
Definition:
Standard deviation of returns measures the average deviation of a stock’s returns from its mean return over a given period. In other words, it shows how spread out the returns are around the average.

High σ → returns deviate strongly from the average → stock is more volatile / risky
Low σ → returns are close to the average → stock is more stable

Practical Cases: Beta vs Standard Deviation
🔹 Case 1: High beta + high volatility

- Aggressive stock
- Strongly reacts to market movements
- Typical growth / tech

    Example: Tesla, Nvidia

🔹 Case 2: Low beta + low volatility

- Defensive
- Stable
- Good for hedging / defensive portfolios

    Example: Utilities, Consumer Staples

🔹 Case 3: Low beta + high volatility

- Specific / idiosyncratic risk
- News-driven fluctuations
- Diversification helps

    Example: Biotech, small caps

🔹 Case 4: High beta + low volatility

- “Efficient market leverage”
- Rare, very attractive

    Example: Occasionally some large-cap, stable tech stocks
                """
            )
        with st.expander("Sharpe Ratio definition, click to expand"):
            st.write(
                """

Sharpe Ratio shows how much extra return you get for the risk you take.
A higher Sharpe means better reward for the asset risk.


Zero Sharpe = risk-free rate (Rf)


- Sharpe Ratio is calculated as:

Sharpe =( 𝑅 − 𝑅𝑓 ) / 𝜎

Where:

R = return of the asset

Rf= risk-free rate

σ = standard deviation of returns

- Interpretation:

Sharpe = 0 → the asset earns exactly the risk-free rate (no risk premium)

Sharpe < 0 → the asset performs worse than the risk-free rate

Sharpe > 0 → the asset provides a positive risk-adjusted return

- Colors interpretation 

Color indicates whether the asset outperforms the risk-free rate.
Color intensity reflects the strength of risk-adjusted performance.


Color	                 Sharpe Range	   Meaning

🔴 Red	                Sharpe < 0	       Risk not rewarded

🔘 Gray (Neutral) 	    0 = Sharpe   	   Zero risk premium / Neutral zone

🟢 Green	            Sharpe ≥ 0         Good risk-return relationship


"""
            )
        with st.expander(" Pearson Correlation (r) definition, click to expand"):
            st.write(
                """
                    What does it measure?
                    How strongly and linearly two instruments move together.
                    Range: from –1 to +1.

                    +1 → they move in the same direction, perfectly

                    0 → no linear relationship

                    –1 → they move in opposite directions

                    Most important: Correlation tells you only about the direction and consistency of movement, but not how many units something increases or decreases.

                    Example:
                    If the S&P 500 goes up by 1% → Apple often also goes up by around 1%
                    → high correlation (e.g., 0.9)
                    But we still don’t know whether Apple increases more or less.
            """
            )
        with st.expander("R² (the coefficient of determination), click to expand"):
            st.write("""
In finance, R² (the coefficient of determination) is a measure that shows how well an explanatory variable (e.g., a benchmark or index) explains the variability of an asset’s returns.

In other words, it indicates what portion of a portfolio’s or stock’s return variability is explained by the variability of the benchmark.

Interpretation:

High Beta

- R² = 0.95 → 95% of the stock’s return variability is driven by the market/benchmark.

- 1 − R² = 0.05 → only 5% of the variability is specific to the company.

The stock reacts strongly to market movements.

Low Beta

- R² = 0.20 → only 20% of the variability is explained by the benchmark.

- 1 − R² = 0.80 → 80% of the variability comes from other factors.

The stock moves relatively independently of the market.
                         """)


@staticmethod
def new_list_with_benchmark(selected_symbols, benchmark):
    benchm = benchmark
    symbols = selected_symbols
    symbols_with_benchmark = symbols
    symbols_with_benchmark.append(benchm)
    return symbols_with_benchmark
