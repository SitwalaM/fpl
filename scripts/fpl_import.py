# Module containing several functions for pulling data from the FPL API

from numpy import nan
import pandas as pd 
import requests 
import json
import numpy as np


def get_raw_fpl_tables(url = 'https://fantasy.premierleague.com/api/bootstrap-static/'):
  # returns jason data from the FPL API

  r = requests.get(url)
  json_data = r.json()
  return json_data
 

def combine_player_teams(raw_json, min_minutes = 1):
    '''
    returns a pandas dataframe with all FPL data for each player
    input: raw json data from FPL API, minimum minutes for players
    output: dictionary of pandas dataframes of player data and team_data

    '''
    elements_df = pd.DataFrame(raw_json['elements'])
    elements_types_df = pd.DataFrame(raw_json['element_types']) 
    teams_df = pd.DataFrame(raw_json['teams'])

    # cut some of the info in the elements df
    slim_elements_df = elements_df[["id",'second_name','team','element_type','selected_by_percent',
                                   'now_cost','minutes','transfers_in','value_season','total_points',
                                   'ict_index', "web_name", "form"]].copy()

    # get positions from the elements_types dataframe
    slim_elements_df['position'] = slim_elements_df.element_type.map(elements_types_df.set_index('id').singular_name)

    # get team names 
    slim_elements_df['team'] = slim_elements_df.team.map(teams_df.set_index('id').name)

    # make sure value columns are float
    slim_elements_df['value'] = slim_elements_df.copy().value_season.astype(float)
    slim_elements_df['form'] = slim_elements_df.copy().form.astype(float)

    #filter minimum minutes for players
    slim_elements_df = slim_elements_df.loc[slim_elements_df.minutes >= min_minutes]

    return {"player_data": slim_elements_df, "team_data": teams_df}


def get_player_hist(player_id ):
    '''             
    function gets player historical data for the season
    input: player_id a
    output: historical player data in json format 

    '''
    url = 'https://fantasy.premierleague.com/api/element-summary/' + \
          str(player_id) + '/'

    response = requests.get(url)
    response = json.loads(response.content)  
    fixtures = response['fixtures']
    history = response['history']
    history_past = response['history_past']
    return history


def combine_all_players_hist(player_id):
    '''
    input: player_ids of players to be combined for historical data
    output: dataframe of player historical data (gameweek to gameweek performance)
    '''

    history = get_player_hist(player_id.iloc[0])
    all_players_hist = pd.DataFrame(history)

    for player in player_id.iloc[1:]:
      history = get_player_hist(player)
      player = pd.DataFrame(history)
      all_players_hist = pd.concat([all_players_hist,player], axis = 0)
    return all_players_hist


def compute_player_variation(all_players_hist, min_minutes = 1, top_number = 100):
    '''
    calculates player averages and volatility in performance
    input: all players historical data, minimum minutes and how many players to filter_out(top_number)
    output: dataframe with player FPL average points and coefficient of variation
    '''
    
    grouped_mean  = all_players_hist.loc[all_players_hist.minutes>0].groupby(by = "element").mean().total_points
    grouped_std = all_players_hist.loc[all_players_hist.minutes>0].groupby(by = "element").std().total_points
    player_variation = pd.DataFrame({"Mean": grouped_mean, "Std": grouped_std })

    player_variation["player"] =  player_variation.index
    player_variation["CV"] =  player_variation.Std/player_variation.Mean
    player_variation =  player_variation.nlargest(top_number, "Mean")

    raw_json = get_raw_fpl_tables()
    slim_elements_df = combine_player_teams(raw_json, min_minutes)
    slim_elements_df = slim_elements_df['player_data'] 

    # map the names using the element ID
    map_columns = ["second_name", "position", "ict_index", "minutes", "now_cost", "team"]
    for map_string in map_columns:
      player_variation[map_string] = player_variation.player.map(slim_elements_df.set_index("id")[map_string])

    player_variation["now_cost"] = player_variation.now_cost/10
    player_variation =   player_variation.dropna()

    
    return player_variation


def get_team_fixtures():
    '''
    returns all the league fixture data from the FPL site
    '''
    url = "https://fantasy.premierleague.com/api/fixtures/"
    r = requests.get(url)
    json = r.json()
    fixtures = pd.DataFrame(json)
    fixtures =  fixtures[fixtures.event.notnull()]
    return fixtures

def get_current_gameweek():
    # returns the current active gameweek event 
    data = get_team_fixtures()
    data = data[data.finished == True]
    current_gameweek = data.event.max()

    return current_gameweek



