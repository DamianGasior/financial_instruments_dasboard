from api_request_alphavantage import Underlying_request_details
from pipeline import UnderlyingBuilder
from collections import deque


def main():
    
    queue_of_requests=deque()

    symbol_deque=deque(['MSFT','AMD','GOOGL'])
  
    if len(symbol_deque) ==0:
        raise ValueError('Missing Underlyin code')
    else:
        while symbol_deque:#trigger it till is not empty

            underlying_reuqestor=Underlying_request_details(
            symbol= symbol_deque.popleft(),
            function="TIME_SERIES_DAILY",
            outputsize="compact",
            datatype="json")
            queue_of_requests.append(underlying_reuqestor)

            


    

    while queue_of_requests:
        underlying_reuqestor=queue_of_requests.popleft()
        pipeline_builder=UnderlyingBuilder(underlying_reuqestor)
        pipeline_builder.run_pipeline(underlying_reuqestor)
        if not queue_of_requests: # will go through the loop only one time. 
            pipeline_builder.run_merged_df_pipeline()
    

if __name__=="__main__":
    main()