from api_request_alphavantage import Underlying_request_details
from single_data_frame import Underlying_data_frame
from metrics_calcs import Underlying_metrics
from multiple_data_frame import Dataframe_combine_builder
import pandas as pd


multiple_data_frame=Dataframe_combine_builder() ## tu jakostotreba rozwiazac 
result_worst_and_best=Dataframe_combine_builder() #ht
corr_data_frame=Dataframe_combine_builder()




class UnderlyingBuilder:
    def __init__(self,underlying_reuqestor:Underlying_request_details,df_builder_result:Dataframe_combine_builder |None=None):
        self.underlying_reuqestor=underlying_reuqestor

        if  self.underlying_reuqestor.function=="TIME_SERIES_DAILY":
            self.key_paremeter="Time Series (Daily)"
        #will be expanded with other key.parametrs like for week and monthly
            self.df_builder_result=df_builder_result
        
        

    def run_pipeline(self,underlying_reuqestor) :
        stock=self.underlying_reuqestor.request_to_ext_api()
        print(type(stock))
        data_frame_builder =Underlying_data_frame(stock,self.key_paremeter,underlying_reuqestor)
        print('Type for  "data_frame_builder" is : ',type(data_frame_builder))
        

        multiple_data_frame.add_to_list(data_frame_builder)
    
        data_frame_builder_with_calcs=Underlying_metrics(self.underlying_reuqestor,data_frame_builder) #this was key , passing here the class parameters , and dataframe
        print(data_frame_builder_with_calcs.price_chng_perct())
        print(data_frame_builder_with_calcs.head())  
        print(type(data_frame_builder))
        print(type(data_frame_builder_with_calcs))

        data_frame_builder_corr=data_frame_builder_with_calcs.copy_df()
        # data_frame_builder_corr.copy_df()
        # print(data_frame_builder_corr.head())
        print(type(data_frame_builder_corr))
        corr_data_frame.add_to_list(data_frame_builder_corr)

        worst_and_best=data_frame_builder_with_calcs.worst_and_best()
        print(worst_and_best)
        print(type(worst_and_best))
        result_worst_and_best.add_to_list(worst_and_best)

        stand_deviation_metrics=data_frame_builder_with_calcs.std_dev()
        print(stand_deviation_metrics)

    def run_merged_df_pipeline(self):


        multiple_data_frame.multiple_data_frame_creator('multiples')
        print(multiple_data_frame)
        print(type(multiple_data_frame))

# put later the results of this on a matplotlib ,  on x there will be months / days, on y will be the reurun  
        result_worst_and_best.multiple_data_frame_creator('worst_and_best')
        print(result_worst_and_best)

        print(corr_data_frame.calc_correlation('correlation'))






