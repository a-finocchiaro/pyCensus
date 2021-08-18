import pandas as pd
import requests

# construct dataframe of ALL API endpoints from the Census Bureau
all_endpoints_raw = requests.get("https://api.census.gov/data.json")
all_endpoints_df = pd.json_normalize(all_endpoints_raw.json()['dataset'])

# append column with 'accessURL' for each
all_endpoints_df['accessURL'] =  pd.json_normalize(all_endpoints_raw.json()['dataset'], record_path=['distribution'])['accessURL']
