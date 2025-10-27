import pandas as pd
from single_data_frame import Underlying_data_frame
from metrics_calcs import Underlying_metrics




class Dataframe_combine_builder:
    def __init__(self,single_data_frame:Underlying_data_frame | None=None):
        
        self.set_of_df = {}
        self.frames=[]


    def add_to_list(self,single_data_frame):
        
        if isinstance(single_data_frame,pd.DataFrame):
            self.frames.append(single_data_frame)

        else:
            self.single_data_frame=single_data_frame.to_dataframe()
            print(type(self.single_data_frame))
            print(self.single_data_frame.head())
            self.frames.append(single_data_frame)
            return self.single_data_frame




 #create a method which takes all the ifnromation from the list  and does combine that into one. 
    def multiple_data_frame_creator(self,name_of_set):
       #this method allows to put all dataframes into a dictionary, you can search in the dict using values like 'worst_and_best'
    #    print('MultipleDataFrame')  # for log  dev purpose
       self.final_df=pd.concat(self.frames,axis=1)
       self.set_of_df[name_of_set]= self.final_df
       return self.final_df




    def __str__(self):
        print('Multiple data frame print')
        return str (self.final_df)
   

    def calc_correlation(self,name):
        request_for_df=self.multiple_data_frame_creator(name)
        corr_result=request_for_df.corr()
        return corr_result

       
