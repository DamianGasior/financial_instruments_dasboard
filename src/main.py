from src.api_providers.alpha_vantage.api_request_alphavantage import (
    Underlying_request_details,
)
from src.pipeline.pipeline import UnderlyingBuilder, DataPipeline
from collections import deque
import streamlit as st
from src.api_providers.finhub import finhub_websocket
from src.api_providers.twelve_data.api_request_twelve_data import (
    Underlying_twelve_data_reuquest,
)
from src.api_providers.common import utils, multiple_data_frame
from src.metrics.metrics_calcs import Underlying_metrics
from src.api_providers.finhub.finhub_python import Finhub_data_builder

# st.session_state.my_merged_list = ["PHYS", "AEM"]


if "multi_builder" not in st.session_state:
    st.session_state.multi_builder = multiple_data_frame.Dataframe_combine_builder()

if "metrics_instance" not in st.session_state:
    st.session_state.metrics_instance = Underlying_metrics()








def main():

    if st.session_state.my_merged_list:

        # print(st.session_state.my_list)
        queue_of_requests = deque()
        td_queue_of_requests = deque()  # twelve_data_queue

        symbol_deque = deque(st.session_state.my_merged_list)
        #    symbol_deque=deque(['PHYS', 'AEM','GDX','FNV'])
        print("symbol_deque", symbol_deque)

        if len(symbol_deque) == 0:
            raise ValueError("Missing Underlyin code")
        else:
            while symbol_deque:  # trigger it till is not empty

                # symbol = symbol_deque.popleft()

                # if st.session_state.selected_broker == "Alpha vantage":
                #     underlying_reuqestor = Underlying_request_details(
                #         symbol=symbol,
                #         function=st.session_state.price_type,
                #     )
                #     print("underlying_reuqestor", underlying_reuqestor)
                #     underlying_reuqestor.read_all_keys_values_from_api()
                #     # underlying_reuqestor.read_caches()
                #     queue_of_requests.append(underlying_reuqestor)
                #     print("queue_of_requests", queue_of_requests)

                # elif st.session_state.selected_broker == "Alpha vantage_test":

                #     #new logic , to use BASE API PRovider abstract class, dokonczyc data trasnform dla alpha vantage,a potem dac
                #     function=st.session_state.price_type
                #     provider=Underlying_request_details(symbol,function) # symbol = 'AEM',function = 'TIME_SERIES_DAILY'
                #     pipeline_instance=DataPipeline(provider,symbol)
                #     multi,metrics = pipeline_instance.run()

                #     # st.session_state.all_multi.append(multi)
                #     # st.session_state.all_metrics.append(metrics)

                if st.session_state.selected_broker == "Twelve data":
                    print(symbol_deque)
                    symbol = symbol_deque.popleft()
                    print(symbol)
                    provider = Underlying_twelve_data_reuquest(symbol)
                    pipeline = DataPipeline(
                        provider=provider,
                        symbol=symbol,
                        multi=st.session_state.multi_builder,
                        metrics=st.session_state.metrics_instance,
                    )
                    pipeline.run()

                    print("test twelve data")
                    pass

        if st.session_state.selected_broker == "Alpha vantage":
            while queue_of_requests:
                underlying_reuqestor = queue_of_requests.popleft()
                pipeline_builder = UnderlyingBuilder(underlying_reuqestor)
                pipeline_builder.run_pipeline()
                if not queue_of_requests:  # will go through the loop only one time.
                    pipeline_builder.run_merged_df_pipeline()
                if not queue_of_requests:  # will go through the loop only one time.
                    pipeline_builder.run_merged_df_pipeline()
        elif st.session_state.selected_broker == "Twelve data":
            while td_queue_of_requests:
                requested_underlying = td_queue_of_requests.popleft()

            print("test twelve data")
            pass

    else:
        st.warning("No data found — please poput and submit the data again")


if __name__ == "__main__":
    main()
