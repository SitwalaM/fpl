# function that handles fixtures difficulty data for each team

import pandas as pd 
import numpy as np

from fpl_import import *

# get current gameweek details for default values
gameweek = get_current_gameweek()


def team_difficulty(gameweek_A=gameweek+1, gameweek_B=gameweek+4):
    '''
    returns the difficulty of fixtures faced so far
    input: gameweek_A to gameweek_B are integers determing the range to be considered for difficulty
    output: dataframe showing each team and the total difficulty for the number of gameweeks specified
    '''
    raw_json = get_raw_fpl_tables()
    teams_df = combine_player_teams(raw_json)

    fixtures = get_team_fixtures()
    fixtures =  fixtures[(fixtures.event <= gameweek_B) & (fixtures.event >= gameweek_A)] 
  
    index = 0
    output_df = pd.DataFrame(columns = ["event","team_id","opponent_id", "home/away", "opponent_difficulty","number_games"])
    
    for event in list(fixtures.event.unique()): 
        
        filter_event = fixtures[fixtures["event"]== event].copy()
        teams_list = list(filter_event.team_a) + list(filter_event.team_h)

        teams = []
        [teams.append(x) for x in teams_list if x not in teams]
        
        
        for team in teams:
            # triple gameweek logic not accounted for yet here, to be improved
            if (team in list(filter_event.team_a)) and (team in list(filter_event.team_h)):
                opponent_id = [filter_event[filter_event["team_a"]==team].team_h.values, \
                        filter_event[filter_event["team_h"]==team].team_a.values] 

                opponent_difficulty = [filter_event[filter_event["team_a"]==team].team_a_difficulty.values, \
                                filter_event[filter_event["team_h"]==team].team_h_difficulty.values]                   
                home = [False, True] 
           
            
            elif team in list(filter_event.team_a):
                opponent_id = filter_event[filter_event["team_a"]==team].team_h.values  
                opponent_difficulty = filter_event[filter_event["team_a"]==team].team_a_difficulty.values
                home = False
                
            else:
                opponent_id = filter_event[filter_event["team_h"]==team].team_a.values
                opponent_difficulty = filter_event[filter_event["team_h"]==team].team_h_difficulty.values
                home = True

            
            output_df.loc[index,"event"] = event
            output_df.loc[index,"team_id"] = team
            output_df.loc[index,"opponent_id"] = np.array(opponent_id).flatten().tolist()
            output_df.loc[index,"home/away"] = np.array(home).flatten()
            output_df.loc[index,"opponent_difficulty"] = np.array(opponent_difficulty).flatten().sum()
            output_df.loc[index,"number_games"] = len(output_df.loc[index,"opponent_id"])

            index += 1
        
    
    # filter the dataframe
    output_df =  output_df[(output_df.event <= gameweek_B) & (output_df.event >= gameweek_A)]  

    # Add team names
    output_df['team'] = output_df.team_id.map(teams_df['team_data'].set_index('id').name)
    output_df_sums =   output_df.groupby("team", as_index = False).sum()
    output_df_sums =  output_df_sums[["team","opponent_difficulty", "number_games"]]

    return {'teams_list': output_df, "totals": output_df_sums}
                            

data = team_difficulty()

data = data["totals"]





    
                        
