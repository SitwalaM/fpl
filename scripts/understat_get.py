#gets xG data from the understat site

import requests
import pandas as pd
import datetime as dt
from fpl_import import get_current_gameweek

def get_understat_players(season="2021", full_season = True, n_last_matches = "4"):
    # pulls understat FPL data and returns dataframe

    with requests.Session() as s:
        if full_season == True:
            data = {
                "league": "EPL",
                "season": season
            }
            column_append = "_full_season"
        else:
            data = {
                "league": "EPL",
                "season": season,
                "n_last_matches": n_last_matches,
            }
            column_append = "_last_"+ n_last_matches + "_matches"
        resp = s.post("https://understat.com/main/getPlayersStats/", data=data)
    json_data =  resp.json()["response"]["players"]
    xg_df = pd.DataFrame.from_dict(json_data, orient='columns')

     

    #format float columns and rename columns to show if full season or n_last games
    strings = ["player_name", "team_title", "position"]
    columns = xg_df.columns
    new_colmns = [] 
    for column in columns:
        if column not in strings:
            xg_df[column] = xg_df[column].astype(float)
            new_col = column + column_append
            xg_df.rename({column:new_col}, axis = 1, inplace = True)

    player_map = pd.read_csv("ID_map.csv")
    player_map  = player_map[["fpl_id","understat_id"]]
    player_map = player_map[player_map.understat_id != 0]
    xg_df["fpl_id"] =  xg_df[xg_df.columns[0]].map(player_map.set_index("understat_id").fpl_id)
    
    return xg_df

gameweek = get_current_gameweek()
datestr = dt.datetime.today().strftime("%Y%m%d")
data = get_understat_players(season="2022", full_season = True, n_last_matches = "4")
data.to_csv("../data/undestat_full_gw{}_{}.csv".format(int(gameweek),datestr))


