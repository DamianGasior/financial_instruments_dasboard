import streamlit as st
import numpy as np
import pandas as pd
from src import pipeline
from src import metrics_calcs


def correlation_helper(df_list):
    merged_df_sec = pd.concat(df_list, axis=1)
    correlation_summary = metrics_calcs.Underlying_metrics.calc_correlation(
        merged_df_sec
    )
    return correlation_summary
