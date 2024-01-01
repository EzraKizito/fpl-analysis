import requests, json
from pprint import pprint
import pandas as pd
from tqdm.auto import tqdm
tqdm.pandas()

""" Important information about the FPL API is found here:
https://gist.githubusercontent.com/James-Leslie/82abbb4c6808321b0cf8c801a84ff22e/raw/9b5a238a52159d8e856adcc2aa18a734b9178561/FPL-endpoints.csv
"""

""" The FPL API is a RESTful API that returns JSON data. The base URL for all
FPL API endpoints is https://fantasy.premierleague.com/api/. The API is
publicly available, and does not require authentication. The API is updated
periodically throughout the season, and the data is available for personal
use. The API is rate limited to 100 requests per minute per IP address."""

""" The code in this file is based on the following tutorial: 
https://medium.com/analytics-vidhya/getting-started-with-fantasy-premier-league-data-56d3b9be8c32
"""

# base url for all FPL API endpoints
base_url = 'https://fantasy.premierleague.com/api/'

# get data from bootstrap-static endpoint
r = requests.get(base_url+'bootstrap-static/').json()

# Write a function that obtains the gameweek history for a given player
# Modify to integrate optional argument for a specific gameweek in the past.
def get_gameweek_history(player_id):
    '''get all gameweek info for a given player_id'''
    
    # send GET request to
    # https://fantasy.premierleague.com/api/element-summary/{PID}/
    r = requests.get(
            base_url + 'element-summary/' + str(player_id) + '/'
    ).json()
    
    # extract 'history' data from response into dataframe
    df = pd.json_normalize(r['history'])
    
    return df

# Write a function that obtains the season history for a given player
def get_season_history(player_id):
    '''get all past season info for a given player_id'''
    
    # send GET request to
    # https://fantasy.premierleague.com/api/element-summary/{PID}/
    r = requests.get(
            base_url + 'element-summary/' + str(player_id) + '/'
    ).json()
    
    # extract 'history_past' data from response into dataframe
    df = pd.json_normalize(r['history_past'])
    
    return df

# show the top level fields
pprint(r, indent=2, depth=1, compact=True)

players = r['elements']

pd.set_option('display.max_columns', None)

# create players dataframe
players = pd.json_normalize(r['elements'])

# create teams dataframe
teams = pd.json_normalize(r['teams'])

# get position information from 'element_types' field
positions = pd.json_normalize(r['element_types'])

# join players to teams
df = pd.merge(
    left=players,
    right=teams,
    left_on='team',
    right_on='id'
)

# join player positions
df = df.merge(
    positions,
    left_on='element_type',
    right_on='id'
)

# rename columns
df = df.rename(
    columns={'name':'team_name', 'singular_name_short':'position_name'}
)
 
# show result
player_bio = df[['id','first_name', 'second_name','web_name', 'team_name', 'position_name', 'element_type']]
team_names = player_bio['team_name'].unique().tolist()

# show player #5's gameweek history
get_gameweek_history(5)

df.loc[5, ['web_name']]

# show player #1's gameweek history
get_season_history(501).head(13)

 
# select columns of interest from players df
players = players[
    ['id', 'first_name', 'second_name', 'web_name', 'team',
     'element_type', 'position_name']
]

# join team name
players = players.merge(
    teams[['id', 'name']],
    left_on='team',
    right_on='id',
    suffixes=['_player', None]
).drop(['team', 'id'], axis=1)

# join player positions
players = players.merge(
    positions[['id', 'singular_name_short']],
    left_on='element_type',
    right_on='id'
).drop(['element_type', 'id'], axis=1)

players.head()

# get gameweek histories for each player
points = players['id_player'].progress_apply(get_gameweek_history)

# combine results into single dataframe
points = pd.concat(df for df in points)

# join web_name
points = players[['id_player', 'web_name']].merge(
    points,
    left_on='id_player',
    right_on='element'
)

 
# get top scoring players by gameweek 19
halfway_leaders = points.groupby(
    ['element', 'web_name']
).agg(
    {'total_points':'sum', 'goals_scored':'sum', 'assists':'sum'}
).reset_index(
).sort_values(
    'total_points', ascending=False
)

 
points