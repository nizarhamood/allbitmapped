'''
THIS IS NOW REDUNDANT AS I AM NOW USING IT DIRECTLY IN THE CALLBACK FUNCTION IN d_component.py

API from Coin Ranking

SSL: WRONG_VERSION_NUMBER error due to Turkey location, need VPN connection
'''
import requests
import pandas as pd
import matplotlib.pyplot as plt


url = "https://api.coinranking.com/v2/coins" # URL for api call on the coins data


'''
By setting the timeperiod the change percentage and sparkline in the response will be calculated accordingly


Default value: 24h
Allowed values: 
3h 24h 7d 30d 3m 1y 3y 5y
'''


coin_limit = 50 # RANGE 0 - 100
time_period = "24h" # In the d_component.py file this comes from the user

'''
# ADD FOLLOWING: 
    * Add the below filter options in website
        defi 
        stablecoin
        nft
        dex
        exchange
        staking
        dao
        meme
        privacy
'''

tags_coin_type = [
        'defi', 
        'stablecoin',
        'nft',
        'dex',
        'exchange',
        'staking',
        'dao',
        'meme',
        'privacy'
]


#tags_coin_type = 'nft' # Using this for test delet or comment afterwards


#Below are the list to be returned for the coins kpi
kpi_query = {
    "referenceCurrencyUuid":"yhjMzLPhuIDl",
    "timePeriod":time_period,
    "tags": tags_coin_type, # NEED TO ADD THIS TO THE USER OPTION
    "tiers":"1",
    "orderBy":"marketCap",
    "orderDirection":"desc",
    "limit":str(coin_limit),
    "offset":"0"
}


headers = {
	"X-RapidAPI-Host": "coinranking1.p.rapidapi.com",
	"X-RapidAPI-Key": "coinrankinge1773ef837002a546df6cbc3fe022129656c5697b85e5774"
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

'''
BELOW IS FOR THE ICONS TO SHOW IN THE DATA TABLE, THIS HAS NOW BEEN PLACED INTO THE DATATABLE AND IS IN THE d_component.py FILE


# For loop to create html image tags to be used in the d_component.py file
img_src = []
for x in coins_display['iconUrl']:
    img_link = f'<img src="{x}" style="height: 30px; width:30px;"/>'
    img_src.append(img_link)


# Create a new column in the dataframe for using in the DataTable in the d_component.py file
coins_display['icons'] = img_src

# Remove duplicates 
coins_display = coins_display.drop_duplicates(subset=['name'])
#coins_display.to_csv(f'coins_display{time_period}.csv')

'''


'''
# Include Sparkline
display_sparkline_coins_column = [
    "name",
    "sparkline",
]


sparkline_coins_display = coins_df[display_sparkline_coins_column]

#sparkline_coins_display.to_csv('data/sparkline_coins_display.csv', index=False)

# To turn the sparkline column into a numeric for graphing
sparkline_coins_display['sparkline'] = pd.to_numeric(sparkline_coins_display['sparkline'])


#Create a for loop to create images and save them into static/matlplotlib for use the the DataTable
#Improve the line graph look and feel


for x in sparkline_coins_display['sparkline']:
    #plt.plot(sparkline_coins_display[x], text=x)
    plt.axis('off')
    plt.savefig(f"static/matplotlib/{x}.png", dpi=300)
'''