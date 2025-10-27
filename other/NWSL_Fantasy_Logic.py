# NWSL Fantasy Logic
from typing import Union
from fastapi import FastApi
from pydantic import BaseModel

nwsl_json = "nwsl_2025_season.json"

# Points system
# Goal F:4 M:5 D:6
# Assist:3
# Clean Sheet M:1 D:5
# Goal Conceded D: -1 per 2
# Yellow: -1
# Red: -3
# Save: GK:1 per 3
# Penalty Save: 5
# Penalty Miss: -2
# Own Goal: -2
# Minutes Played: 1pt <60, 2pt >=60
# Bonus: 1st:3, 2nd:2, 3rd:1
# Defensive Bonus: Tackles, Clearances, Interceptions, Ball Recoveries: 2 pt >8 total per game





def calculate_fantasy_points(row, position):
    points = 0
    minutes = row.get("minutes", 0)
    goals = row.get("goals", 0)
    assists = row.get("assists", 0)
    clean_sheet = row.get("clean_sheets", 0)
    goals_conceded = row.get("goals_conceded", 0)
    yellow_cards = row.get("yellow_cards", 0)
    red_cards = row.get("red_cards", 0)
    saves = row.get("saves", 0)
    penalty_saves = row.get("penalty_saves", 0)
    penalty_misses = row.get("penalty_misses", 0)
    own_goals = row.get("own_goals", 0)
    defensive_actions = sum([row.get(stat, 0) for stat in ["tackles_summary", "clearances_defense", "interceptions_summary", "ball_recoveries_misc"]])
    # bonus_points = row.get("bonus_points", 0)

    # Minutes Played
    if minutes >= 60:
        points += 2
    elif minutes > 0:
        points += 1

    # Goals Scored
    if position == "F":
        points += goals * 4
    elif position == "M":
        points += goals * 5
    elif position == "D":
        points += goals * 6
    elif position == "GK":
        points += goals * 6

    # Assists
    points += assists * 3

    # Clean Sheets
    if position in ["D", "GK"]:
        points += 5
    elif position == "M":
        points += 1

    # Goals Conceded
    if position in ["D", "GK"]:
        points -= (goals_conceded // 2) * 1

    # Cards
    if red_cards == 0:
        points -= yellow_cards * 1
    else:
        points -= red_cards * 3

    # Saves
    if position == "GK":
        points += (saves // 3) * 1

    # Penalty Saves and Misses
    points += penalty_saves * 5
    points -= penalty_misses * 2

    # Own Goals
    points -= own_goals * 2

    # Defensive Actions Bonus
    if position in ["CB", "RB", "LB", "WB", "M", "GK"] and defensive_actions >= 8:
        points += 2
    elif position in ["F", "RW", "LW", "AM"] and defensive_actions >= 10:
        points += 2
    
    # Bonus Points
    # points += bonus_points

    return points