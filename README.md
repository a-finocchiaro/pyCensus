# PyCensus

The pyCensus module is designed to interact with the United States Census Bureau API. It handles making the request to the api, and transforms the returned data into a pandas dataframe.

## Prerequisites and Installation

This requires Python 3.7 or later to be installed. 

```
pip install pycensus
```

## Setup

This tool is not yet designed to be used with an API key, but that is something that could easily be added in the future.

## Shell Scripts

PyCensus comes with shell scripts to parse the online API documentation and allow it to be searched easily by the user. 

search all endpoints:

```
census-endpoints [year] [column to search]
```
available_columns:
- c_vintage = year
- c_dataset = Dataset identifier
- title
- description

search variables, geographies, or groups for an endpoint:

```
census-variables [year] [dataset]
census-geography [year] [dataset]
census-groups [year] [dataset]
```

This can be used to parse the variables, geography, or groups sheets available for a specific endpoint. 

An example is below:

```
census-geography 2019 acs acs5 profile
```

## censusData

censusData gets data from the Census Bureau api based on certain attributes given when an object is instatiated.

Input attributes:
- `dataset` = list; The list of abbreviations for the dataset name path. This can be found by going to the https://api.census.gov/data.html page or running find-endpoint and using the value in the "Dataset Name" column. 
- `year` = int; the Year that corresponds to the chosen dataset.
- `query_dict` = dict; The dict of how the query should be structured. This should include any other necessary pieces to construct the query like "for" and "in". See the examples for the chosen dataset for help with constructing a query.

Below is an exmaple of how acsData could be instantiated:

```python
test_data = censusData(
                ['acs', 'acs5', 'profile'],
                2019,
                {
                    'get' : 'group(DP03)',
                    'in' : 'state:04',
                    'for' : 'county:019,007'
                }
    )
```

### censusData.clean_df

This produces a pandas dataframe from the Census Bureau data and replaces the column names with names that explain what the data point is. 

Input arguments:
- `index_col` = str; The column that should be the index column
- `replace_col_names` = bool; `True` will replace column names with the variable names, `False` will leave columns named with variable ID.

Returns:
    Pandas Dataframe