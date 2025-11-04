import pandas as pd
from src.single_data_frame import Underlying_data_frame
from src.metrics_calcs import Underlying_metrics




class Dataframe_combine_builder:
    def __init__(self,single_data_frame:Underlying_data_frame | None=None):
        
        self.set_of_df = []
        self.single_stock_with_prices={}
        self.dict_of_dict={}
        self.single_df=[]



    def add_to_dict(self,single_data_frame,stock_symbol):
        # creating a copy so that in case are other operations done on single_data_frame, other columns added in this case I will see only prices
        single_data_frame=single_data_frame.copy()  
        
        if isinstance(single_data_frame,pd.DataFrame):
           self.single_stock_with_prices[stock_symbol] = single_data_frame
           return self.single_stock_with_prices
           
        else:
            self.single_data_frame=single_data_frame.to_dataframe()
            self.single_stock_with_prices[stock_symbol] = self.single_data_frame
            return self.single_stock_with_prices
    
   
    def add_dict_to_dcit(self,single_dict, name):
       self.dict_of_dict[name]=single_dict
       print(self.dict_of_dict)
       return self.dict_of_dict
    

#tbc if it will work for self.single_stock_with_prices={} and for  self.dict_of_dict={}
    def get_the_right_df(self,stock):
       value =  self.single_stock_with_prices[stock]
       print(value)
       return value 
    
    def get_the_right_dict(self,name):
       specifc_dict =  self.dict_of_dict[name]
       print(specifc_dict)
       return specifc_dict 
    







 #create a method which takes all the ifnromation from the list  and does combine that into one. 
    def multiple_data_frame_creator(self,name_of_set):
       #this method allows to put all dataframes into a dictionary, you can search in the dict using values like 'worst_and_best'
    #    print('MultipleDataFrame')  # for log  dev purpose
       self.final_df=pd.concat(self.frames,axis=1)
       self.set_of_df[name_of_set]= self.final_df
       print(type(self.final_df))
       print(self.final_df)
       return self.final_df
    

    def attach_df_to_list_concac(self,value):
        #this method allows to put all dataframes into a dictionary, you can search in the dict using values like 'worst_and_best'
        #    print('MultipleDataFrame')  # for log  dev purpose
        self.single_df=pd.concat(value,axis=1)
        # self.set_of_df[name_of_set]= self.final_df
        print(type(self.final_df))
        print(self.single_df)
        return self.final_df



    def show_content(self):
        print( f'key length : {len(self.dict_of_dict.keys())}, value length : {len(self.dict_of_dict.values())}')
        for key,value in self.dict_of_dict.items(): 
            print(f'key is : {key}, -> value is :  {type(value)} ')

        
        print( f'key length : {len(self.single_stock_with_prices.keys())}, value length : {len(self.single_stock_with_prices.values())}')
        for key1,value1 in self.single_stock_with_prices.values():
                print(f'key1 is : {key1} -> {type(value1)}')

 

    def __str__(self):
        info='Cotent of this data frame: \n'
        for att_name,value in self.__dict__.items():
            if isinstance(value,dict):
                info += f'- {att_name} : {len(value)} DataFrame -> {list(value.keys())}\n'
        return info

    def calc_correlation(self,name):
        request_for_df=self.multiple_data_frame_creator(name)
        corr_result=request_for_df.corr()
        return corr_result
    

    def __getitem__(self, key):
        return getattr(self, key, None) 

       
