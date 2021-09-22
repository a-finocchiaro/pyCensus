"""
Command line utility to search the available API endpoints from the Census Bureau. Prints them out in a command line table. 

CLI Args:

    - text = str; The string to search for in a column.
    - col = str; the column to be searched

"""
import argparse
import re
import pandas as pd
import requests
from rich.console import Console
from rich.table import Table

def main():
    """
    Constructs dataframe, parses CLI args passed, and prints the result to the terminal in a table.
    """
    # construct dataframe of ALL API endpoints from the Census Bureau
    all_endpoints_raw = requests.get("https://api.census.gov/data.json")
    all_endpoints_df = pd.json_normalize(all_endpoints_raw.json()['dataset'])

    # append column with 'accessURL' for each, convert c_vintage column to int and then string to search it
    all_endpoints_df['accessURL'] =  pd.json_normalize(all_endpoints_raw.json()['dataset'], record_path=['distribution'])['accessURL']
    all_endpoints_df['c_vintage'] = all_endpoints_df.c_vintage.astype('Int64').astype(str)

    # parse cli args
    ap = argparse.ArgumentParser()
    ap.add_argument('text', nargs=None, type=str, help='the string to search column values for.')
    ap.add_argument('column', nargs='?', type=str, help='The column to search.', default="title")
    args = ap.parse_args()
    text, col = args.text, args.column

    # filter based on search terms
    if re.search(r"dataset", col):
        filtered_df = all_endpoints_df[all_endpoints_df.c_dataset.apply(lambda x: text in x)]
    else:
        filtered_df = all_endpoints_df[all_endpoints_df[col].str.contains(text)]

    # return data to console in table
    table = Table(title="Census API Endpoints")
    table.add_column("Title", justify="right", style="cyan")
    table.add_column("Dataset Name", justify="right", style="yellow")
    table.add_column("Year", justify="right", style="purple")
    table.add_column("Description", justify="right", style="green")
    table.add_column("URL", justify="right")

    for row in filtered_df.iterrows():
        table.add_row(row[1]['title'],
                      ', '.join(row[1]['c_dataset']),
                    #   str(row[1]['c_vintage']).rstrip('.0'),
                      row[1]['c_vintage'],
                      row[1]['description'],
                      row[1]['accessURL'])

    console = Console()
    console.print(table)

if __name__ == '__main__':
    main()
