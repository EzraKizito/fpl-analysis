import requests, json
from pprint import pprint
import pandas as pd
from tqdm.auto import tqdm
import random
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
r_bootstrap = requests.get(base_url+'bootstrap-static/').json()

# get data from managers endpoint — sample with manager 10000
r_mh = requests.get(base_url+'entry/'+'10000'+'/history/').json()

season_experience = len(pd.json_normalize(r_mh['past']))
 
random.seed(1)
manager_sample = random.sample(range(1, 10000000), 100)       
