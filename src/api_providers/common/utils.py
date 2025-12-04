import pandas as pd
from datetime import date


def set_date_as_index(df_from_api_provider):
    print('test',df_from_api_provider)
    # df_from_api_provider.index.name = (
    #     "Date"  # assiging the name of the columns as 'Date' which is our index
    # )
    df_from_api_provider=df_from_api_provider.set_index("datetime")
    print('test1',df_from_api_provider)
    df_from_api_provider.index.name="Date" # changine the name of index column to "Date"
    print('test2',df_from_api_provider)

    df_from_api_provider.index = pd.to_datetime(df_from_api_provider.index).date
    print('test3',df_from_api_provider)
    # self.response_from_alpha.index=self.response_from_alpha.index.dt.date  <<this will not work
    # changing the columns ( apart of date one ) to int or float
    for col in df_from_api_provider:
        if not pd.api.types.is_datetime64_any_dtype(df_from_api_provider[col]):  # function is checking if each colums is not in a datetime format, if its not, then : 
            df_from_api_provider[col] = pd.to_numeric(df_from_api_provider[col], errors="coerce" )  # applying the change and convert to a number , "coerce"  means if the value can not be changed to number, convert to NaN
    return df_from_api_provider




def column_rename(df_from_api_provider, **kwargs):
    # columns #thnink if it should be alist or a dict or waht ?
    df_from_api_provider.rename(columns=kwargs, inplace=True)
    return df_from_api_provider


def leave_only_columns(df_from_api_provider, *args):
    chosen_columns = []
    for column in args:
        chosen_columns.append(column)
    df_from_api_provider = df_from_api_provider[chosen_columns]
    print(df_from_api_provider)
    return df_from_api_provider

