# main script that produces all the data files used

import pandas as pd 

from difficulty import team_difficulty
from fpl_import import *
from understat_get import *

# function calls
gameweek = get_current_gameweek()
raw_json = get_raw_fpl_tables()
slim_elements_df = combine_player_teams(raw_json)
slim_elements_df = slim_elements_df["player_data"]
player_id = slim_elements_df.id
all_players_hist = combine_all_players_hist(player_id)
player_variation = compute_player_variation(all_players_hist)
ouput_df = team_difficulty(1,gameweek)
ouput_df = ouput_df["totals"]
player_variation["total_FDR_so_far"] = player_variation.team.map(ouput_df.set_index("team").opponent_difficulty)


ouput_df_1 = team_difficulty(gameweek+1,gameweek+3)
ouput_df_1 = ouput_df_1["totals"]
player_variation["next_four_fixtures_FDR"] = player_variation.team.map(ouput_df_1.set_index("team").opponent_difficulty)
player_variation["number_of_games"] = player_variation.team.map(ouput_df_1.set_index("team").number_games)

#save CSV files
datestr = dt.datetime.today().strftime("%Y%m%d")
slim_elements_df.to_csv("../data/main_fpl_{}.csv".format(datestr))
player_variation.to_csv("../data/player_variation_{}.csv".format(datestr))




