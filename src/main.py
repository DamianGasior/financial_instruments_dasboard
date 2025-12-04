from src.api_providers.alpha_vantage.api_request_alphavantage import Underlying_request_details
from src.pipeline.pipeline import UnderlyingBuilder
from collections import deque
import streamlit as st
from src.api_providers.finhub import finhub_websocket
from src.api_providers.twelve_data import api_request_twelve_data,to_dataframe_transofmer
from src.api_providers.common import utils


# st.session_state.my_merged_list = ["PHYS", "AEM"]


def main():

    if st.session_state.my_merged_list:

        # print(st.session_state.my_list)
        queue_of_requests = deque()
        td_queue_of_requests = deque() # twelve_data_queue
        

        symbol_deque = deque(
            st.session_state.my_merged_list
        )  #    symbol_deque=deque(['PHYS', 'AEM','GDX','FNV'])
        print("symbol_deque", symbol_deque)
        if len(symbol_deque) == 0:
            raise ValueError("Missing Underlyin code")
        else:
            while symbol_deque:  # trigger it till is not empty
                if st.session_state.selected_broker == "Alpha vantage":
                    underlying_reuqestor = Underlying_request_details(
                        symbol=symbol_deque.popleft(),
                        function=st.session_state.price_type,
                        outputsize="compact",
                        datatype="json",
                    )
                    print('underlying_reuqestor',underlying_reuqestor)
                    underlying_reuqestor.read_all_keys_values_from_api()
                    # underlying_reuqestor.read_caches()
                    queue_of_requests.append(underlying_reuqestor)
                    print("queue_of_requests", queue_of_requests)

                elif st.session_state.selected_broker == "Twelve data":
                    requested_underlying=api_request_twelve_data.Underlying_twelve_data_details(
                        symbol=symbol_deque.popleft()
                    )
                    td_queue_of_requests.append(requested_underlying)
                    print('test twelve data')
                    pass


        if st.session_state.selected_broker == "Alpha vantage":
            while queue_of_requests:
                underlying_reuqestor = queue_of_requests.popleft()
                pipeline_builder = UnderlyingBuilder(underlying_reuqestor)
                pipeline_builder.run_pipeline(underlying_reuqestor)
                if not queue_of_requests:  # will go through the loop only one time.
                    pipeline_builder.run_merged_df_pipeline()
                if not queue_of_requests:  # will go through the loop only one time.
                    pipeline_builder.run_merged_df_pipeline()
        elif st.session_state.selected_broker == "Twelve data":
            while td_queue_of_requests:
                requested_underlying = td_queue_of_requests.popleft()


            print('test twelve data')
            pass


    else:
        st.warning("No data found — please poput and submit the data again")


if __name__ == "__main__":
    main()
