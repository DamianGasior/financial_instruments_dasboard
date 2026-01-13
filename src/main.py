from src.api_providers.alpha_vantage.api_request_alphavantage import (
    Underlying_request_details,
)
from src.pipeline.pipeline import DataPipeline
from collections import deque
import streamlit as st
from src.api_providers.twelve_data.api_request_twelve_data import (
    Underlying_twelve_data_reuquest,
)
from src.api_providers.common import multiple_data_frame
from src.metrics.metrics_calcs import Underlying_metrics
from src.api_providers.finhub.finhub_python import Finhub_data_builder

import logging

from src.session_init import init_session_state

# st.session_state.my_merged_list = ["PHYS", "AEM"]


# if "multi_builder" not in st.session_state:   << dalem do pliku 1_Mulitple_symbols.py - zoabczymy czy tam zadzia;a
#     st.session_state.multi_builder = multiple_data_frame.Dataframe_combine_builder()


def main():
    init_session_state()

    if st.session_state.my_merged_list:

        # # print(st.session_state.my_list)
        # queue_of_requests = deque()
        # td_queue_of_requests = deque()  # twelve_data_queue

        symbol_deque = deque(st.session_state.my_merged_list)
        #    symbol_deque=deque(['PHYS', 'AEM','GDX','FNV'])
        print("symbol_deque", symbol_deque)

        if len(symbol_deque) == 0:
            raise ValueError("Missing Underlyin code")
        else:
            while symbol_deque:  # trigger it till is not empty

                if st.session_state.selected_broker == "Twelve data":
                    print(symbol_deque)
                    symbol = symbol_deque.popleft()
                    print(symbol)
                    provider = Underlying_twelve_data_reuquest(
                        symbol,
                        adjust=st.session_state.price_type,
                        interval=st.session_state.price_type,
                    )
                    pipeline = DataPipeline(
                        provider=provider,
                        symbol=symbol,
                        multi=st.session_state.multi_builder,
                        metrics=st.session_state.metrics_instance,
                    )
                    pipeline.run()

                    print("test twelve data")
                    pass

                elif st.session_state.selected_broker == "Alpha vantage_test":
                    print(symbol_deque)
                    symbol = symbol_deque.popleft()
                    print(symbol)
                    provider = Underlying_request_details(
                        symbol=symbol, function=st.session_state.price_type
                    )
                    pipeline = DataPipeline(
                        provider=provider,
                        symbol=symbol,
                        multi=st.session_state.multi_builder,
                        metrics=st.session_state.metrics_instance,
                    )
                    pipeline.run()

                    print("Alpha vantage_test")
                    pass

    else:
        st.warning("No data found — please poput and submit the data again")


if __name__ == "__main__":
    main()
