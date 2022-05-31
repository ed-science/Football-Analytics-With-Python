# -*- coding: utf-8 -*-
"""
load_data.py
-----------
Created on Wed Apr 15 21:54:09 2020

@author: slothfulwave612

This Python module will help to load the 
Statsbomb's competition and match data.

Here we will take the football match between
Real Madrid and Barcelona from La Liga 2008-09
played at Santiago Bernabeu, the result ended at 2-6.

And then we will display all the result of Barcelona for
La Liga Season 2008-09 season from the data present in the dataset.

Modules Used(1):
---------------
1. json -- module to work with JSON data.
"""

import json        ## importing json module

## loading the competitions.json file 
with open('../Statsbomb/data/competitions.json') as comp_file:
    comp_data = json.load(comp_file)

## if you will see the comp_data you will find
## that the La Liga 2008-09 competition has id number 11
## and the season id is 41
comp = 11
season_id = 41

## load all the matches from this competition
with open(f'../Statsbomb/data/matches/{comp}/{season_id}.json') as match_file:
    match_data = json.load(match_file)

## now finding home team and away team
## home team: Real Madrid
## away team: Barcelona
## match id: None(set by default)
home_team = 'Real Madrid'
away_team = 'Barcelona'
match_id = None
score = None

## iterating through each match to find the match_id
for match in match_data:
    home_team_value = (match['home_team']['home_team_name'] == home_team)
    away_team_value = (match['away_team']['away_team_name'] == away_team)

    if home_team_value and away_team_value:
        match_id = match['match_id']
        score = str(match['home_score']) + ' : ' + str(match['away_score'])

## checking if the match is found or not
## if found then displaying the right result
if match_id != None:
    print(f'{home_team} vs {away_team} has match id: {match_id}')
    print(f'Score: {score}')
else:
    print('No match found')

## let's try to find all the results for Barcelona for
## La Liga season 2008-09
for match in match_data:
    home_team_value = match['home_team']['home_team_name']
    away_team_value = match['away_team']['away_team_name'] 

    if home_team_value == 'Barcelona' or away_team_value == 'Barcelona':
        score = str(match['home_score']) + ' : ' + str(match['away_score'])
        print(f'{home_team_value} vs {away_team_value}, score: {score}')
