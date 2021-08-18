"""
Includes various search functions to help simplify locating data to request.
"""
import pandas as pd
import requests
import urllib.parse as urlparse
from pyCensus import all_endpoints_df
from rich.console import Console
from rich.table import Table

def find_endpoint(text='', col='title'):
    """
    Gets all available API endpoints from the Census website and puts them into a Pandas
    dataframe. Then searches the dataframe for a matching string.
    """
    # filter based on search terms
    filtered_df = all_endpoints_df[all_endpoints_df[col].str.contains(text)]

    # return data to console in table
    table = Table(title="Census API Endpoints")
    table.add_column("Title", justify="right", style="cyan")
    table.add_column("Dataset Name", justify="right", style="yellow")
    table.add_column("Year", justify="right", style="purple")
    table.add_column("Description", justify="right", style="green")
    table.add_column("URL", justify="right")

    for index,row in filtered_df.iterrows():
        table.add_row(row['title'],
                      ', '.join(row['c_dataset']),
                      str(row['c_vintage']).rstrip('.0'),
                      row['description'],
                      row['accessURL'])

    console = Console()
    console.print(table)

def request_data(year:int, dataset_name:list, dataset_info:str):
    """
    gets variables, geography, groups, or examples for any API endpoint
    """
    base_url = "https://api.census.gov/data/"
    query_url = f"{base_url}{year}/{'/'.join(dataset_name)}/{dataset_info}.json"

    results = requests.get(query_url)
    return results.json()

def get_variables(year:int, dataset_name:list):

    json_data = request_data(year, dataset_name, 'variables')

    df = pd.DataFrame(json_data['variables']).transpose()

    # set NaN values to string values of 'None'
    df = df.where(pd.notnull(df), str(None))

    # make table
    table = Table(title="Variables")
    table.add_column("Variable", justify="right", style="cyan")
    table.add_column("Label", justify="right", style="Green")

    for index,row in df.iterrows():
        table.add_row(index,
                      row['label'])
    
    console = Console()
    console.print(table)

def get_geography(year:int, dataset_name:list):

    json_data = request_data(year, dataset_name, 'geography')

    df = pd.DataFrame(json_data['fips'])
    
    # set NaN values to string values of 'None'
    df = df.where(pd.notnull(df), str(None))

    # make table
    table = Table(title="Geography Options")
    table.add_column("GeoLevel Code", justify="right", style="cyan")
    table.add_column("Name", justify="right", style="Green")
    table.add_column("Requires", justify="right", style="Purple")

    for index,row in df.iterrows():
        table.add_row(row['geoLevelDisplay'],
                      row['name'],
                      ', '.join(row['requires']) if type(row['requires']) == list else row['requires'])
    
    console = Console()
    console.print(table)

def get_groups(year:int, dataset_name:list):

    json_data = request_data(year, dataset_name, 'groups')

    df = pd.DataFrame(json_data['groups'])
    
    # set NaN values to string values of 'None'
    df = df.where(pd.notnull(df), str(None))

    # make table
    table = Table(title="Groups")
    table.add_column("Name", justify="right", style="cyan")
    table.add_column("Description", justify="right", style="Green")

    for index,row in df.iterrows():
        table.add_row(row['name'],
                      row['description'])
    
    console = Console()
    console.print(table)
