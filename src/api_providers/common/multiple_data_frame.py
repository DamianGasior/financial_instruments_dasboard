import pandas as pd
from src.api_providers.alpha_vantage.single_data_frame import Underlying_data_frame
from src.metrics.metrics_calcs import Underlying_metrics
from src.api_providers.twelve_data.to_dataframe_transofmer import (
    Underlying_twelve_data_details,
)


class Dataframe_combine_builder:
    def __init__(self, single_data_frame: Underlying_data_frame | None = None):

        # self.set_of_df = []
        self.single_stock_data = {}
        self.dict_of_dict = {}
        self.merged_list = []
        # multiple_data_frame=None
        # self.multiple_dicts = None
        # self.response_from_api=response_from_api
        # self.merged_list = []

    def add_to_dict(self, single_data_frame, stock_symbol):
        # creating a copy so that in case are other operations done on single_data_frame, other columns added in this case I will see only prices
        single_data_frame = single_data_frame.copy()
        print(type(single_data_frame))

        if isinstance(single_data_frame, pd.DataFrame):
            self.single_stock_data[stock_symbol] = single_data_frame
            print("len of add_to_dict1:", len(self.single_stock_data))
            print(type(self.single_stock_data))
            return self.single_stock_data

        else:
            # self.single_data_frame = single_data_frame.to_dataframe()
            self.single_data_frame = single_data_frame.to_frame()
            self.single_stock_data[stock_symbol] = self.single_data_frame
            print("len of add_to_dict2:", len(self.single_stock_data))
            print(type(self.single_stock_data))

            return self.single_stock_data

    def add_dict_to_dcit(self, single_dict, name):
        self.dict_of_dict[name] = single_dict
        print(self.dict_of_dict)
        self.dict_of_dict
        print("len of self.dict_of_dict", len(self.dict_of_dict))
        return self.dict_of_dict

    # tbc if it will work for self.single_stock_data={} and for  self.dict_of_dict={}
    def get_the_right_df(self, stock):
        value = self.single_stock_data[stock]
        print(value)
        return value

    def get_the_right_dict(self, name):
        print("Klucze dostępne:", self.dict_of_dict.keys())
        print("Szukany klucz name:", name)
        specifc_dict = self.dict_of_dict[name]
        print(specifc_dict)
        print(type(specifc_dict))
        return specifc_dict

    def execute_operation(self, df_with_price, symbol):
        # multiple_dicts = Dataframe_combine_builder()
        symbol_name = symbol
        multiple_dict=self.add_to_dict(df_with_price, symbol_name)
        print("test1")
        self.add_dict_to_dcit(multiple_dict, "single_prices")
        print("test2")

    #  #create a method which takes all the ifnromation from the list  and does combine that into one.
    #     def multiple_data_frame_creator(self,name_of_set):
    #        #this method allows to put all dataframes into a dictionary, you can search in the dict using values like 'worst_and_best'
    #     #    print('MultipleDataFrame')  # for log  dev purpose
    #        self.final_df=pd.concat(self.frames,axis=1)
    #        self.set_of_df[name_of_set]= self.final_df
    #        print(type(self.final_df))
    #        print(self.final_df)
    #        return self.final_df

    #     def attach_df_to_list_concac(self, value):
    #         #this method allows to put all dataframes into a dictionary, you can search in the dict using values like 'worst_and_best'
    #         #    print('MultipleDataFrame')  # for log  dev purpose
    #         self.single_df=pd.concat(value, axis=1)
    #         # self.set_of_df[name_of_set]= self.final_df
    #         print(type(self.final_df))
    #         print(self.single_df)
    #         return self.final_df

    def show_content(self):
        print(
            f"key length : {len(self.dict_of_dict.keys())}, value length : {len(self.dict_of_dict.values())}"
        )
        for key, value in self.dict_of_dict.items():
            print(f"key is : {key}, -> value is :  {type(value)} ")

        print(
            f"key length : {len(self.single_stock_data.keys())}, value length : {len(self.single_stock_data.values())}"
        )
        for key1, value1 in self.single_stock_data.values():
            print(f"key1 is : {key1} -> {type(value1)}")

    def __str__(self):
        info = "Cotent of this data frame: \n"
        for att_name, value in self.__dict__.items():
            if isinstance(value, dict):
                info += (
                    f"- {att_name} : {len(value)} DataFrame -> {list(value.keys())}\n"
                )
        return info

    # adding a dictionary to a list :

    # passed_dict = {'PHYS':              PHYS
    #               2025-11-17  30.73
    #               2025-11-14  31.16
    #               2025-11-13  31.71
    #               2025-11-12  3...
    #               2025-06-27  25.01
    # so  later  it can be extracted so a comboined dataframe with prices can be built
    # @staticmethod
    def list_merger(self, passed_dict, list_of_symbols):
        # merged_list = []

        for symbol in list_of_symbols:
            if symbol not in passed_dict.keys():
                break
            elif symbol in passed_dict.keys():
                value = passed_dict[symbol]
                if any(df.equals(value) for df in self.merged_list):
                    break
                else:
                    self.merged_list.append(passed_dict[symbol])
        return self.merged_list

    def __getitem__(self, key):
        return getattr(self, key, None)

    @staticmethod
    def list_concacenate(df_lists):
        concac_lists = pd.concat(df_lists, axis=1).sort_index(ascending=False)
        concac_lists = concac_lists.fillna(method="ffill").fillna(method="bfill")
        return concac_lists
