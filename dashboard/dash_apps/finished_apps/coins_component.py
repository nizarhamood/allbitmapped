'''
API from CoinRanking.com

SSL: WRONG_VERSION_NUMBER error due to Turkey location, need VPN connection
'''
import requests
import pandas as pd
import matplotlib.pyplot as plt

'''
Below are the modules for the Dash Components
'''

import dash
from dash import dash_table, dcc, html, Input, Output
from dash.dash_table import FormatTemplate
from dash.dash_table.Format import Format, Sign

from django_plotly_dash import DjangoDash

#from data.data import coins_display

#coins_df = coins_display.to_dict('records') # Has to be in dict with records to work with the Data Tables

app = DjangoDash('coins')   # DjangoDash replaces dash.Dash

'''
API CALL AND DATA PROCESSING 
'''
url = "https://api.coinranking.com/v2/coins" # URL for api call on the coins data


'''
DATA TABLE SETTINGS BELOW
'''

# Dropdown menu options which affects the % change and sparkline
time_period = [
    '3h',
    '24h',
    '7d',
    '30d',
    '3m',
    '1y',
    '3y',
    '5y',
]

# Dropdown menu options which for different groups of coins
tags_coin_type = {
        'DeFi': 'deFi', 
        'Stable Coins': 'stablecoin',
        'NFT': 'nft',
        'Decentralized Exchange':'dex',
        'Exchange': 'exchange',
        'Staking': 'staking',
        'Decentralized autonomous organizations': 'dao',
        'Meme Coins': 'meme',
        'Private Coins':'privacy'
}

kpi_query = {
    "referenceCurrencyUuid":"yhjMzLPhuIDl",
    "tiers":"1",
    "orderBy":"marketCap",
    "orderDirection":"desc",
    "offset":"0"
}



price_money = FormatTemplate.money(2) # For Coin price
market_cap_money = FormatTemplate.money(0)


# Column id/name and general formatting
columns_format = [
    dict(id = 'icons', name = '', presentation='markdown'),
    dict(id = 'symbol', name=''),
    dict(id = 'name', name='Coins'),
    dict(id = 'price', name='Price', type='numeric', format=price_money),
    #dict(id = 'sparkline', name='Sparkline', type='numeric', format=price_money),
    dict(id = 'change', name='% Change', type='numeric', format=Format(sign=Sign.positive)),
    dict(id = 'marketCap', name='Market Cap', type='numeric', format=market_cap_money),
    dict(id = '24hVolume', name='Volume (24 hour)', type='numeric', format= Format().group(True))
]

# Column Style Formatting
style_data_conditionals = [
    {
        'if': {
            'filter_query': '{change} < 0',
            'column_id': 'change'
        },
        'color': 'tomato',
        'font_weight': 'bold'
    },
    {
        'if': {
            'filter_query': '{change} >= 0',
            'column_id': 'change'
        },
        'color': 'rgb(60, 179, 113)',
        'font_weight': 'bold'
    },
    {
        'if': {'column_id': 'symbol'},
        'textAlign': 'left',
        'width': 100
    },
    {
        'if': {'column_id': 'icons'},
        'width': 40
    },
    {
        'if': {'column_id': 'price'},
        'width': 150
    },
    {
        'if': {'column_id': 'sparkline'},
        'width': 150
    },
]

style_data = {
        'height': 'auto'
}

# Cell Formatting
style_cell = {
    'max_width': 15,
    'textAlign': 'right',
    'textOverflow': 'ellipsis'
}

# DataTable and Dropdown menu list

app.layout = html.Div([
    html.Div([
        dcc.Dropdown( # Dropdown for coin types
        id='coin_type',
        options=[
        {'label': 'All Coins', 'value': 'all', },
        {'label': 'DeFi', 'value': 'deFi', },
        {'label': 'Stable Coins', 'value': 'stablecoin',},
        {'label': 'NFT', 'value': 'nft',},
        {'label': 'Decentralized Exchange', 'value':'dex',},
        {'label': 'Exchange', 'value': 'exchange',},
        {'label': 'Staking', 'value': 'staking',},
        {'label': 'Decentralized autonomous organizations', 'value': 'dao',},
        {'label': 'Meme Coins', 'value': 'meme',},
        {'label': 'Private Coins', 'value':'privacy'},
        ],
        value="all",
        placeholder='Please Select Coin Type',
        ),
        dcc.Dropdown( # Dropdown for Coins time period
        id='coins_time_period',
        options=time_period,
        value="24h",
        placeholder='Please Select Time-Frame',
        ),
    ]),
    dash_table.DataTable( # Coins DataTable
        id = 'coins_table',
        markdown_options = {
            'html': True
        },
        fixed_rows = {
            'headers': True
        },
        columns = columns_format,
        style_data = style_data,
        style_cell = style_cell,
        style_data_conditional = style_data_conditionals,
        style_as_list_view = True,
        export_columns = 'all',
        export_format = 'csv',
    ),
    html.Div([], id = "test_div")
])

@app.callback(
    Output('coins_table', 'data'),
    Input('coins_time_period', 'value'),
    Input('coin_type', 'value'),
)
def update_output(coins_time_period, coin_type):
    # I had to do the data processing in the function to be able to use the callback function value to change the time period. Before I had a separate file for this
    
    coin_limit = 50 # I've limited the number of coins to a maximum of 50 (I may increase this later, or give the user the option to change it)

    kpi_query.update(
        {
            "limit": str(coin_limit),
            "timePeriod":coins_time_period
        }
    )

    #Below are the list to be returned for the coins kpi
    if coin_type == 'all':
        kpi_query
    else:
        kpi_query["tags"] = coin_type
        kpi_query


    headers = {
    	"X-RapidAPI-Host": "coinranking1.p.rapidapi.com",
    	"X-RapidAPI-Key": "coinrankinge1773ef837002a546df6cbc3fe022129656c5697b85e5774" # Free public API don't worry
    }


    #Ordered by marketCap (Highest - Lowest)
    response = requests.request("GET", url, headers=headers, params=kpi_query)
    # Reads the request into the data_txt variable
    data_txt = response.text


    # Converts the data request into a pandas dataframe object
    data_df = pd.read_json(data_txt)
    data_df.to_csv('data_df.csv')


    # Begin the cleaning process by exploding the 'data' column
    df_exp = data_df.explode('data')
    df_exp.to_csv('df_exp.csv')


    # Iterate through the 'data' column for each item
    my_variables = {}
    i = 0
    for x in df_exp['data']:
        i += 1
        if isinstance(x, dict): # To only perform below if the object is a dictionary object
            my_variables["data_exp_" + str(i)] = x # Creates a new variable for each dictionary


    #This is a function to use in a for loop
    def dict_to_df(data_exp):
        # To be used in a for loop to convert multiple dicts into dataframes
        data_exp = pd.DataFrame.from_dict(my_variables[str(data_exp)])
        return data_exp


    # Uses the dict_to_df function to append a list of dataframes 
    data_frame_list = []
    for x in my_variables:
        data_frame_list.append(dict_to_df(x)) # Appends the dataframe to a list by using the dict_to_df function


    coins_df = pd.concat(data_frame_list, ignore_index=True) # Concatenate all the dataframes together


    coins_df.to_csv('coins_df.csv')


    display_coins_columns = [
        "iconUrl",
        "symbol",
        "name",
        "price",
        "change",
        "marketCap",
        "24hVolume"
    ]


    coins_display = coins_df[display_coins_columns]


    # Convert all numbers columns into numberic to be used in DataTable in d_component.py
    for x in coins_display:
        if x != 'iconUrl' and x != 'symbol' and x != 'name':
            coins_display[x] = pd.to_numeric(coins_display[x])


    # For loop to create html image tags to be used in the d_component.py file
    img_src = []
    for x in coins_display['iconUrl']:
        img_link = f'<img src="{x}" style="height: 30px; width:30px;"/>'
        img_src.append(img_link)


    # Create a new column in the dataframe for using in the DataTable in the d_component.py file
    coins_display['icons'] = img_src


    # Remove duplicates 
    coins_display = coins_display.drop_duplicates(subset=['name'])


    coins_df = coins_display.to_dict('records')

    # So the variable isn't stored with the updated keys and value pairs once the function is called 
    kpi_query.clear()


    return coins_df


