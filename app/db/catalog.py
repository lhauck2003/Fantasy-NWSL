## catalog classes
import sqlite3


class Catalog():
    def __init__(self):
        self.__conn = sqlite3.connect('data/nwsl_fantasy.db')
        self.__cursor = self.__conn.cursor()

    def fetch(self, row):
        pass
    def sort(self, column_name):
        pass
    def filter(self, column_name, value):
        pass

    ## access the database
    def add(self, item:list):
        pass
    def remove(self, item):
        pass
    def update(self, row, column, value):
        pass
    def get_catalog(self):
        pass
    def get_table(self, table_name):
        request =  f"""
                    SELECT * FROM {table_name}
                    """
        return self.__cursor.execute(request)

class Player:    
    def __init__(self, stats: dict):
        self.__stats: dict = stats

    def get_column_value(self, column):
        return self.__stats[column]
    
    def sort_by_stat(self, column):
        return self.get_column_value(column)
    def filter(self, column_name, value):
        if(self[column_name]==value):
            return self
        return None

class PlayerList(Catalog):
    def __init__(self):
        self.__players:list[Player] = []

    def fetch(self, row) -> Player:
        return self.__players[row]
    
    def sort(self, column_name):
        self.__players.sort(Player.sort_by_stat(column_name))

    def filter(self, column_name, value) -> list:
        filtered_players = []
        for player in self.__players:
            test_player = player.filter(column_name, value)
            if test_player == None:
                pass
            else:    
                filtered_players.append(test_player)
        return filtered_players
    
    def add(self, item):
        pass
    def remove(self, item):
        pass
    def update(self, row, column, value):
        pass
    def get_catalog(self):
        self.__players = [] #initialize to empty
        self.__players = Catalog.get_table("players")


class FNWSL_Team:
    points: int
    name: str
    players: list = []
    def sort_by_stat(self, column):
        return self.points
    def filter(self, column_name, value):
        if(self[column_name]==value):
            return self
        return None

class FNWSL_List(Catalog);
    def __init__(self):
        self.__teams: list[FNWSL_Team]

    def fetch(self, row):
        return self.__teams[row]
    
    def sort(self, column_name="points"):
        self.teams.sort(FNWSL_Team.sort_by_stat(column_name))
    
    def filter(self, column_name, value):
        filtered_teams = []
        for team in self.teams:
            test_team = team.filter(column_name, value)
            if test_team == None:
                pass
            else:    
                filtered_teams.append(test_team)
        return filtered_teams
    
    def add(self, item):
        pass
    def remove(self, item):
        pass
    def update(self, row, column, value):
        pass
    def get_catalog(self):
        self.teams = [] #initialize to empty
        self.teams = Catalog.get_table("fnwsl_teams")
    

