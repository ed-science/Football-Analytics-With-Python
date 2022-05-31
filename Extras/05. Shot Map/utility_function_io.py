# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 22:25:10 2020

@author: slothfulwave612

Python module for i/o operations.

Modules Used(4):-
1. numpy -- numerical computing library.
2. pandas -- data manipulation and analysis library.
3. json -- Python library to work with JSON data.
4. sklearn -- machine learning library for the Python programming language.
"""

import pandas as pd
from pandas.io.json import json_normalize
import json

def get_competitions():
    '''
    Function for getting information about each and every
    competitions.
    
    Returns:
    comp_df -- dataframe for competition data.
    '''
    comp_data = json.load(open('../Statsbomb/data/competitions.json'))
    return pd.DataFrame(comp_data)

def flatten_json(sub_str):
    '''
    Function to take out values from nested dictionary present in 
    the json file, so to make a representable dataframe.
    
    ---> This piece of code was found on stackoverflow <--
    
    Argument:
    sub_str -- substructure defined in the json file.
    
    Returns:
    flattened out information.
    '''
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            for i, a in enumerate(x):
                flatten(a, name + str(i) + '_')
        else:
            out[name[:-1]] = x

    flatten(sub_str)
    
    return out

def get_matches(comp_id, season_id):
    '''
    Function for getting matches for the given
    competition id.
    
    Arguments:
    comp_id -- int, the competition id.
    season_id -- int, the season id.
    
    Returns:
    match_df -- dataframe object, containing all the matches 
    '''
    ## setting path to the file
    path = '../Statsbomb/data/matches/{0}/{1}.json'.format(comp_id, season_id)
    
    ## loading up the data from json file
    match_data = json.load(open(path, encoding='utf8'))
    
    ## flattening the json file
    match_flatten = [flatten_json(x) for x in match_data]
    
    ## creating a dataframe
    match_df = pd.DataFrame(match_flatten)
    
    match_df_cols = list(match_df.columns)
    
    ## renaming the dataframe
    for i in range(len(match_df_cols)):
        if match_df_cols[i].count('away_team') == 2:
            ## for away_team columns
            match_df_cols[i] = match_df_cols[i][len('away_team_'):]
        
        elif match_df_cols[i].count('_0') == 1:
            ## for _0 columns
            match_df_cols[i] = match_df_cols[i].replace('_0', '')
        
        elif match_df_cols[i].count('competition') == 2:
            ## for competition columns
            match_df_cols[i] = match_df_cols[i][len('competition_'):]
        
        elif match_df_cols[i].count('home_team') == 2:
            ## for away_team columns
            match_df_cols[i] = match_df_cols[i][len('home_team_'):]
        
        elif match_df_cols[i].count('season') == 2:
            ## for away_team columns
            match_df_cols[i] = match_df_cols[i][len('season_'):]

    match_df.columns = match_df_cols 
        
    return match_df
        
        
def getting_match_id(match_df, req_home_team, req_away_team):
    '''
    Function for getting required match id.
    
    Arguments:
    match_df -- dataframe object, representing the match dataframe.
    req_home_team -- str, required home team.
    req_away_team -- str, required away team.
    
    Returns:
    match_id -- int, the required match id.
    '''

    for row_num, match in match_df.iterrows():
        home_team = match['home_team_name']
        away_team = match['away_team_name']
        
        if home_team == req_home_team and away_team == req_away_team:
            match_id_required = match['match_id']

    return match_id_required

def make_event_df(match_id):
    '''
    Function for making event dataframe.
    
    Argument:
    match_id -- int, the required match id for which event data will be constructed.
    
    Returns:
    event_df -- dataframe object, the event dataframe for the particular match.
    '''
    ## setting path for the required file
    path = f'../Statsbomb/data/events/{match_id}.json'

    ## reading in the json file
    event_json = json.load(open(path, encoding='utf-8'))

    return json_normalize(event_json, sep='_')
      
def full_season_events(match_ids, team_name):
    '''
    Function to make event dataframe for full season for the team
    the player plays in.
    
    Arguments:
    match_id -- list, list of match id.
    team_name -- str, name of the team for which the player plays.
    
    Returns:
    event_df -- dataframe object, containing event data for the whole season.
    '''
    c = 0
    
    for match_id in match_ids:
        temp_df = make_event_df(match_id)
        
        if c == 0:
            event_df = temp_df
            c = 1
        else:
            event_df = pd.concat([event_df, temp_df], sort=True)
    
    event_df = event_df[event_df['team_name'] == team_name]
    
    return event_df

def get_through_balls_id(event_df):
    '''
    Function to get the id associated with a through ball pass in the event dataframe.
    
    Argument:
    event_df -- dataframe object, event data for the whole season.
    
    Returns:
    thorugh_ids -- dict, containing the ids for the thorugh ball pass.
                         key will be the id value will be True.
    '''
    return {
        row['id']: True
        for index, row in event_df.iterrows()
        if (row['pass_goal_assist'] == True)
        & (row['pass_through_ball'] == True)
    }













