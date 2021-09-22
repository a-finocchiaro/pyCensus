"""
Includes various search functions to help simplify locating data to request.
"""
import argparse
import pandas as pd
import requests
from rich.console import Console
from rich.table import Table

def parse_args() -> tuple:
    """
    Parses args for dataset-specific queries.
    returns tuple
    """
    ap = argparse.ArgumentParser()
    ap.add_argument('year', type=int, help='the year corresponding to the dataset')
    ap.add_argument('dataset_name', nargs='+', type=str, help='the json page to get for a dataset.')
    args = ap.parse_args()
    return args.year, args.dataset_name

def request_json(year:int, dataset_name:list, dataset_info:str) -> dict:
    """
    Gets variables, geography, groups, or examples for any dataset.

    input args:
        - year = int; the year that the dataset is from
        - dataset_name = list; th estring path that corresponds to a dataset
        - dataset_info = str; the json page to get for a dataset.

    returns dict
    """
    base_url = "https://api.census.gov/data/"
    query_url = f"{base_url}{year}/{'/'.join(dataset_name)}/{dataset_info}.json"

    results = requests.get(query_url)
    return results.json()

def get_variables():
    """
    Gets all possible variables for a specific dataset.

    input args:
        - year = int; the year that the dataset is from
        - dataset_name = list; th estring path that corresponds to a dataset
    """
    year, dataset_name = parse_args()
    json_data = request_json(year, dataset_name, 'variables')

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

def get_geography():
    """
    Gets all possible geography values for a specific dataset.

    input args:
        - year = int; the year that the dataset is from
        - dataset_name = list; th estring path that corresponds to a dataset
    """
    year, dataset_name = parse_args()
    json_data = request_json(year, dataset_name, 'geography')

    df = pd.DataFrame(json_data['fips'])

    # set NaN values to string values of 'None'
    df = df.where(pd.notnull(df), str(None))

    # make table
    table = Table(title="Geography Options")
    table.add_column("GeoLevel Code", justify="right", style="cyan")
    table.add_column("Name", justify="right", style="Green")
    table.add_column("Requires", justify="right", style="Purple")

    for row in df.iterrows():
        table.add_row(row[1]['geoLevelDisplay'],
                      row[1]['name'],
                      ', '.join(row[1]['requires']) if isinstance(row[1]['requires'], list) else row[1]['requires'])

    console = Console()
    console.print(table)

def get_groups():
    """
    Get all groups for a specific dataset.

    input args:
        - year = int; the year that the dataset is from
        - dataset_name = list; th estring path that corresponds to a dataset
    """
    year, dataset_name = parse_args()
    json_data = request_json(year, dataset_name, 'groups')

    df = pd.DataFrame(json_data['groups'])

    # set NaN values to string values of 'None'
    df = df.where(pd.notnull(df), str(None))

    # make table
    table = Table(title="Groups")
    table.add_column("Name", justify="right", style="cyan")
    table.add_column("Description", justify="right", style="Green")

    for row in df.iterrows():
        table.add_row(row[1]['name'],
                      row[1]['description'])

    console = Console()
    console.print(table)

if __name__=='__main__':
    get_geography()
