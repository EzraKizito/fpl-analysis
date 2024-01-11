from common import *
import numpy as np

# Load data and clean it up
all_players = pd.read_csv("https://github.com/vaastav/Fantasy-Premier-League/blob/master/data/cleaned_merged_seasons.csv?raw=true", low_memory=False)

# all_players.dropna(subset=['team_x'], inplace=True)

