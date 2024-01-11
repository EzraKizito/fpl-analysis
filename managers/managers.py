# Get code from common/common.py:

from common import *

random.seed(1)
manager_sample = random.sample(range(1, 10000000), 100)

manager_past_season_experience = []
manager_past_season_performance = []
manager_current_season_performance = []
manager_past_season_average_rank = []

for manager in tqdm(manager_sample):
    r_manager_history = requests.get(base_url+'entry/'+str(manager)+'/history/').json()
    
    past_manager_history = pd.json_normalize(r_manager_history['past'])
    # past_manager_history['manager_id'] = manager
    # Manager experience - get number of seasons played in FPL
    manager_past_season_experience.append(len(past_manager_history)) 
    
    # Manager current season performance - get average points per gameweek for current season
    try:
        manager_current_season_performance.append(pd.json_normalize(r_manager_history['current'])['points'].sum() / len(pd.json_normalize(r_manager_history['current'])))
    except ZeroDivisionError:
        manager_current_season_performance.append(0) 
         
    if len(past_manager_history) == 0:
        manager_past_season_average_rank.append(0)
        manager_past_season_performance.append(0)
        continue
        
    # Manager average rank per season prior to current season
    try:
        manager_past_season_average_rank.append(past_manager_history['rank'].sum() / len(past_manager_history))
    except ZeroDivisionError:
        manager_past_season_average_rank.append(0)    
    
    # Manager performance — get average points per season prior to current season
    try:
        manager_past_season_performance.append(past_manager_history['total_points'].sum() / len(past_manager_history))
    except ZeroDivisionError:
        manager_past_season_performance.append(0)
        
    
 
# Create dataframe with manager performance data
manager_performance = pd.DataFrame({
                                    'past_season_experience': manager_past_season_experience,
                                    'past_season_performance': manager_past_season_performance,
                                    'past_season_average_rank': manager_past_season_average_rank,
                                    'current_season_performance': manager_current_season_performance},
                                   index=manager_sample
                                   )  

