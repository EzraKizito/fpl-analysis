from common import *

# Get up to date players data. 
"""Obtained from https://github.com/vaastav/Fantasy-Premier-League/blob/master/data/2023-24/cleaned_players.csv"""

player_master_df = pd.read_csv("https://github.com/vaastav/Fantasy-Premier-League/blob/master/data/2023-24/cleaned_players.csv?raw=true")
player_master_df = player_master_df[player_master_df['minutes'] > 0]
# Clean up data

# Classify players by position
goalkeepers = player_master_df[player_master_df['element_type']=="GK"]
defenders = player_master_df[player_master_df['element_type']=="DEF"]
midfielders = player_master_df[player_master_df['element_type']=="MID"]
forwards = player_master_df[player_master_df['element_type']=="FWD"]


