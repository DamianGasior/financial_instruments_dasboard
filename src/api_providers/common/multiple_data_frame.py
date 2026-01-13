import pandas as pd
from src.api_providers.alpha_vantage.single_data_frame import Underlying_data_frame
from src.metrics.metrics_calcs import Underlying_metrics
from src.api_providers.twelve_data.to_dataframe_transofmer import (
    Underlying_twelve_data_details,
)
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)


class Dataframe_combine_builder:
    def __init__(self, single_data_frame: Underlying_data_frame | None = None):

        # self.set_of_df = []
        self.single_stock_data = {}
        self.dict_of_dict = {}
        self.merged_list = []
        self.df_list_for_cut = []
        self.df_dummy_values = []
        self.df_dummy_symbols = []
        self.start_dates = []
        self.end_dates = []

        # multiple_data_frame=None
        # self.multiple_dicts = None
        # self.response_from_api=response_from_api
        # self.merged_list = []

    def add_to_dict(self, single_data_frame, stock_symbol):
        # creating a copy so that in case are other operations done on single_data_frame, other columns added in this case I will see only prices
        single_data_frame = single_data_frame.copy()
        print(type(single_data_frame))
        # self.df_index_allignment2()

        if isinstance(single_data_frame, pd.DataFrame):

            self.single_stock_data[stock_symbol] = single_data_frame

            self.df_index_allignment()

            print("len of add_to_dict1:", len(self.single_stock_data))
            print(type(self.single_stock_data))
            return self.single_stock_data

        else:
            # self.single_data_frame = single_data_frame.to_dataframe()
            self.single_data_frame = single_data_frame.to_frame()

            self.single_stock_data[stock_symbol] = self.single_data_frame
            self.df_index_allignment()

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
        if not self.dict_of_dict.keys(): 
            logging.info("Dictionary is empty")
            return None
        if self.dict_of_dict.keys():
            print("Klucze dostępne:", self.dict_of_dict.keys())
            print("Szukany klucz name:", name)
            specifc_dict = self.dict_of_dict[name]
            print(specifc_dict)
            print(type(specifc_dict))
            if name not in self.dict_of_dict:
                return f'Keys:{name} not found in dict'
        return specifc_dict

    def df_index_allignment(self):
        if len(self.single_stock_data.values()) >= 1:

            for key, value in self.single_stock_data.items():
                logging.info(f"{key} number of rows is {len(value)}")

            # list of the most earliest dates
            self.start_dates = []
            for df in self.single_stock_data.values():
                self.start_dates.append(df.index.min())

            # list of the last dates
            self.end_dates = []
            for df in self.single_stock_data.values():
                self.end_dates.append(df.index.max())

            # common date accross all df's
            start = max(self.start_dates)
            end = min(self.end_dates)

            for key, df in self.single_stock_data.items():
                df_cut = df.loc[start:end]
                self.single_stock_data[key] = df_cut
                logging.info(f"{key} number of rows is {len(value)}")

    def add_aligned_dfs(self):
        self.single_stock_data = dict(zip(self.df_dummy_symbols, self.df_list_for_cut))
        return self.single_stock_data

    def execute_operation(self, df_with_price, symbol):
        # multiple_dicts = Dataframe_combine_builder()

        multiple_dict = self.add_to_dict(df_with_price, symbol)

        self.add_dict_to_dcit(multiple_dict, "single_prices")

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
    # for the below it should be really never used, apart of the pd.concat, the lenght validation is already applied in self.df_index_allignment()

    def list_concacenate(df_lists):
        message = None
        original_lenghts = []

        for df in df_lists:
            lenght_df_list = len(df)
            logging.info(f"received list: {df}")
            logging.info(f"lenght_df_list: {lenght_df_list}")
            original_lenghts.append(lenght_df_list)

        concac_lists = pd.concat(df_lists, axis=1, join="inner").sort_index(
            ascending=False
        )  # autmatically we are cutting evertyhgin to a common index , we keep the rows only those which are common for all Df's

        final_length = len(concac_lists)
        logging.info(f"final_length: {final_length}")

        data_was_cut = False
        for length in original_lenghts:
            if length != final_length:
                data_was_cut = True

        if data_was_cut:
            # list_of_symbols=list(df_lists.columns)
            # print(list_of_symbols)
            # base=df_lists[0].index
            # for i,df in enumerate(df_lists[1:]):
            #     base=base.difference(df.index)

            message = f"Data was cut for one of the incoming datasets,there were  missing information comparing to others. Index alignment applied (join='inner')"

        return concac_lists, message

    #  przekazuje liste z kursami jaki df do correlation_helper gdzie bede potem  werfyikowal
    # uniqe index, potem robie concacente do jednego df, a potem daje jede zloaczaony DF do
    # metrics_calcs.Underlying_metrics.calc_correlation

    #   correlation_helper przerzucic do multiple symbols, a to moze byc w df, choc mialo by sens to liczcy w numpy , sprawdzic czy sie da i jak.  << moze byc w df 
    # jak to bedzie zrobiione to reszta juz bajka bo R2, to jest kwadrat correlation.
    # definicje i co to jest r2 - tutaj : https://chatgpt.com/g/g-p-68e6c9e29bbc8191b9938d8dd6d712f6-mvp/c/695d9385-42ec-832b-b8df-6bf63ea1e3c8

    @staticmethod
    def combined_lists(symbols_from_user, benchmarks):
        # my_merged_list=[]
        my_merged_list = symbols_from_user + benchmarks
        return my_merged_list

    @staticmethod
    def date_index_verfication(df1, df2):
        only_df1 = df1.index.difference(df2.index)
        print(only_df1)
        only_df2 = df2.index.difference(df1.index)
        print(only_df2)
        if df1.index.equals(df2.index) is False:
            print(type(df1))
            print(type(df2))
            common_index = df1.index.intersection(df2.index)
            df1_cut = df1.loc[common_index]
            df2_cut = df2.loc[common_index]
        else:
            return df1, df2

        return df1_cut, df2_cut

    @staticmethod
    def correlation_helper(df_list):
        print(df_list)
        for i in df_list:
            print("unique index:", i.index.is_unique)
            print(i.index.value_counts().head())

        merged_df_sec = Dataframe_combine_builder.list_concacenate(df_list)

        print("test12345")
        print(type(merged_df_sec))
        print(merged_df_sec)
        merged_df_sec = merged_df_sec[0]
        correlation_summary = Underlying_metrics.calc_correlation(merged_df_sec)
        return correlation_summary
    
    @staticmethod
    def first_date(dataframe):
        if dataframe is None or dataframe.empty:
            return None
        else:
            oldest_date = dataframe.index.min()
        return oldest_date

    @staticmethod
    def last_date(dataframe):
        if dataframe is None or dataframe.empty:
            return None
        else:
            newest_date = dataframe.index.max()
        return newest_date

    
    # poszedlbym jednak z numpy stworzy metode ktora dostaje single stock pirces , pobiera dane, liczy return, laczy w jeden df
