"""
censusdata.py

A class designed to create a censusData object and interacts with the Census Bureau API. Once
a censusData object is insantiated, it will dynamically request the data from the API and
create a Pandas dataframe for all of the returned data.
"""
import re
import urllib.parse as urlparse
import pandas as pd
import requests
from pyCensus import BASE_URL

class censusData():
    """
    Requests data from the Census Bureau API and creates a Pandas dataframe to store returned
    data so it can be used for analysis.

    TODO: Add ability to use an API key

    Input Args:
        dataset = list; The list of abbreviations for the dataset name path. This can be found
                    by going to the https://api.census.gov/data.html page or running find-endpoint
                    and using the value in the "Dataset Name" column. 
        year = int; the Year that corresponds to the chosen dataset.
        query_dict = dict; The dict of how the query should be structured. This should include any
                    other necessary pieces to construct the query like "for" and "in". See the
                    examples for the chosen dataset for help with constructing a query.
    """
    def __init__(self, dataset:list, year:int, query_dict:dict):

        self.dataset = dataset
        self.year = year
        self.query_dict = query_dict
        self.raw_acs_data = self._request_data()
        self.df = self._make_df()

    def _request_data(self) -> list:
        """
        Requests data from the census API for the specified endpoint.

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
        Construct a pandas dataframe from the raw json data.

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
            - index_col = str; The column that should be the index column
            - replace_col_names = bool; True will replace column names with the variable names,
                                        False will leave columns named with variable ID.

        returns pandas dataframe
        """
        # deep copy to avoid overwriting original df
        clean_df = self.df.copy()

        # set index
        if index_col:
            clean_df = clean_df.set_index(index_col)

        # get variable names and replace column names with meaningful names
        if replace_col_names:
            if re.search(r"^group", self.query_dict['get']):
                group = re.match(r'(?:^group\((.+)\))', self.query_dict['get'])[1]
                url = f"{BASE_URL}{self.year}/{'/'.join(self.dataset)}/groups/{group}.json"
            else:
                url = f"{BASE_URL}{self.year}/{'/'.join(self.dataset)}/variables.json"

            json_vars = requests.get(url).json()
            name_label_dict = {var:name['label'] for var,name in json_vars['variables'].items()}

            clean_df = clean_df.rename(columns=name_label_dict)

        return clean_df
