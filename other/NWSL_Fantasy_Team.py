# NWSL_Fantasy_Team.py
# Levi Hauck
# 2025
# Classes and logic for managing NWSL Fantasy Teams and Players
# connect to database for player data and stats

import json
from NWSL_Fantasy_Logic import calculate_fantasy_points 

class NWSL_Fantasy_Team:
    def __init__(self, team_name: str, budget:float=100.00):
        self.team_name = team_name
        self.budget = budget
        self.players = []
        self.total_points:int = 0
        self.curr_week_points:int = 0

    def add_player(self, player):
        if player['cost'] <= self.budget:
            self.players.append(player)
            self.budget -= player['cost']
            return True
        return False
    
    def replace_player(self, old_player_id: int, new_player: int):
        if self.remove_player(old_player_id):
            return self.add_player(new_player)
        return False
    
    def remove_player(self, player_id):
        for player in self.players:
            if player['id'] == player_id:
                self.players.remove(player)
                self.budget += player['cost']
                return True
        return False
    
    def calculate_total_points(self):
        self.total_points = sum(player.get('total_points', 0) for player in self.players)
        return self.total_points

    
class Player:
    def __init__(self, name: str, position: str, cost: float):
        self.name = name
        self.position = position
        self.id = None  # to be set when player data is loaded
        self.cost = cost
        self.total_points:int = 0
        self.weekly_points: dict = {}

    def update_points(self, week, points):
        self.weekly_points[week] = points
        self.total_points += points

## Utility function to load players from a JSON file ##
def load_players_from_json(file_path: str):
    with open(file_path, 'r') as f:
        players_data = json.load(f)
    
    players = []
    for pdata in players_data:
        player = Player(
            name=pdata['name'],
            position=pdata['position'],
            cost=pdata['cost']
        )
        player.id = pdata['id']
        player.total_points = pdata.get('total_points', 0)
        player.weekly_points = pdata.get('weekly_points', {})
        players.append(player)
    
    return players