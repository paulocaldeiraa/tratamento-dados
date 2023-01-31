'''Import the packages'''
import uuid
import pandas as pd
import numpy as np

def get_uuid4(
    dataframe:pd.DataFrame,
    check_column_name:str,
    fill_column_name:str)->pd.DataFrame:
    '''
    Use the UUID to generate a random Id.
    employeeID is unique for each employee this ID is a reference for other worksheets.
    All worksheets have a reference ID and another ID of their own.

    1. This function gets the DataFrame where the IDs will be generated.
    2. Name of the column that is used as parameter of the loop.
    3. Name of the column where the generated IDs will be contained.
    '''
    for inx, rows in dataframe.iterrows():
        if rows[check_column_name] != '':
            dataframe.loc[inx, fill_column_name] = uuid.uuid4()


def xlookup(lookup_value,
            lookup_array,
            return_array):
    '''
    In the first line, we are defining a function called xlookup with some arguments.

    lookup_value: the value we are interested, this will be a string value
    lookup_array: this is a column inside the source pandas dataframe,
    we are looking for the “lookup_value” inside this array/column
    return_array: this is a column inside the source pandas dataframe,
    we want to return values from this column
    '''
    match_value = return_array.loc[lookup_array == lookup_value]
    if match_value.empty:
        return np.nan
    else:
        return match_value.tolist()[0]


def replace_str(str_to_replace):
    '''
    This function allows you to remove unwanted characters,
    which appear in the HR worksheet and get in the way
    of creating worksheets of interest
    '''
    str_to_replace = str_to_replace.replace('.','').replace(' ','')
    return str_to_replace
