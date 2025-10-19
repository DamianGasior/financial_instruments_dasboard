from api_request_alphavantage import Underlying_request_details
from pipeline import UnderlyingBuilder
from collections import deque


def main():
    
    queue_of_requests=deque()

    symbol_list=['SPY','MSFT','QQQ']
  

    while symbol_list:
        for code in symbol_list:
            if len(symbol_list) >= 1:
                underlying_reuqestor=Underlying_request_details(
                symbol= symbol_list.pop(0),
                function="TIME_SERIES_DAILY",
                outputsize="compact",
                datatype="json")
            else:
                raise ValueError('Missing Underlyin code')

        queue_of_requests.append(underlying_reuqestor)
        print(len(queue_of_requests))
    

    while queue_of_requests:

        underlying_reuqestor=queue_of_requests.popleft()

        pipeline=UnderlyingBuilder(underlying_reuqestor).run_pipeline(underlying_reuqestor)

    

if __name__=="__main__":
    main()