from src.api_request_alphavantage import Underlying_request_details
from src.pipeline import UnderlyingBuilder
from collections import deque
import streamlit as st


# st.session_state.my_merged_list = ["PHYS","AEM"]


def main():

    # if st.session_state.my_list:
    if st.session_state.my_merged_list:

        # print(st.session_state.my_list)
        queue_of_requests = deque()
        print("queue_of_requests", queue_of_requests)

        symbol_deque = deque(
            st.session_state.my_merged_list
        )  #    symbol_deque=deque(['PHYS', 'AEM','GDX','FNV'])
        print("symbol_deque", symbol_deque)
        if len(symbol_deque) == 0:
            raise ValueError("Missing Underlyin code")
        else:
            while symbol_deque:  # trigger it till is not empty
                underlying_reuqestor = Underlying_request_details(
                    symbol=symbol_deque.popleft(),
                    function="TIME_SERIES_DAILY",
                    outputsize="compact",
                    datatype="json",
                )
                queue_of_requests.append(underlying_reuqestor)

        while queue_of_requests:
            underlying_reuqestor = queue_of_requests.popleft()
            pipeline_builder = UnderlyingBuilder(underlying_reuqestor)
            pipeline_builder.run_pipeline(underlying_reuqestor)
            if not queue_of_requests:  # will go through the loop only one time.
                pipeline_builder.run_merged_df_pipeline()
    else:
        st.warning("No data found — please poput and submit the data again")


if __name__ == "__main__":
    main()
