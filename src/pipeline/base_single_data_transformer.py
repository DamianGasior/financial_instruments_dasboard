from abc import ABC, abstractmethod


class BaseDataTransformer(ABC):

    @abstractmethod
    def transform(self, symbol: str, key_paremeter: str, orient: str):
        pass

    @abstractmethod
    def show_columns(df):
        pass

    @abstractmethod
    def import_symbol():
        pass

    @abstractmethod
    def search_key_param(api_response):
        pass
    
    @abstractmethod
    def set_date_as_index(df_from_api_provider):
        pass

    @abstractmethod
    def column_rename(df_from_api_provider, **kwargs):
        pass


    @abstractmethod
    def leave_only_columns(df_from_api_provider, *args):
        pass

 