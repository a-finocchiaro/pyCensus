"""
pyACS.py
Written by:Aaron Finocchiaro

A class designed to specifically work with the American Community Survey API from census.gov.
"""
import pandas as pd
import re
import requests
import urllib.parse as urlparse
from .search import request_data

BASE_URL = "https://api.census.gov/data/"

class censusData():
    """
        
    """
    def __init__(self, dataset:list, year:int, query_dict:dict):

        self.dataset = dataset
        self.year = year
        self.query_dict = query_dict
        self.raw_acs_data = self._request_data()
        self.df = self._make_df()

    def _request_data(self) -> list:
        """
        Requests data from the census API for the ACS endpoint.

        input args:
            - none

        returns list
        """
        dataset_url = f"{BASE_URL}{self.year}/{'/'.join(self.dataset)}"
        url_parts = list(urlparse.urlparse(dataset_url))
        query = dict(urlparse.parse_qsl(url_parts[4]))
        query.update(self.query_dict)
        url_parts[4] = urlparse.urlencode(query)
        
        raw_acs_data = requests.get(urlparse.urlunparse(url_parts))

        raw_acs_data.raise_for_status()
        return raw_acs_data.json()

    def _make_df(self) -> pd.DataFrame:
        """
        Construct a pandas dataframe from the raw json data from the ACS api call.

        input args:
            - none

        returns pandas dataframe
        """
        df = pd.DataFrame(self.raw_acs_data[1:], columns=self.raw_acs_data[0])
        df = df.loc[:,~df.columns.duplicated()]  #remove duplicate columns
        return df

    def clean_df(self, index_col:str=None, replace_col_names:bool=True) -> pd.DataFrame:
        """
        Replaces the column names with the actual variable names.

        Input arguments:
            - none

        returns pandas dataframe
        """
        # deep copy to avoid overwriting original df
        clean_df = self.df.copy()

        # set index
        if index_col:
            clean_df = clean_df.set_index(index_col)
        
        # get variable names and replace column names with meaningful names
        if replace_col_names:
            group = re.match('(?:^group\((.+)\))', self.query_dict['get'])[1]
            if group:    
                url = f"{BASE_URL}{self.year}/{'/'.join(self.dataset)}/groups/{group}.json"
            else:
                url = f"{base_url}{year}/{'/'.join(dataset_name)}/variables.json"
            
            json_vars = requests.get(url).json()
            name_label_dict = {var:name['label'] for var,name in json_vars['variables'].items()}

            clean_df = clean_df.rename(columns=name_label_dict)

        return clean_df
