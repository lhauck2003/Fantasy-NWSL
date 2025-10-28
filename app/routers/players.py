## Code for displaying a catalog of all the players, ability to sort by a particular stat
import sqlite3

conn  = sqlite3.connect('app/data/nwsl_fantasy.db')

class Players(list):

    def __init__(self, conn=conn):
        self.player_list : list[Player] = conn.execute("SELECT * FROM PLAYERS")

    def display(self):
        for player in self.player_list:
            player.display()
            print("\n---------------------------------------------------------------------------------------------\n")

class Player(dict):
    def __init__(self, player_id: int, conn=conn):
        self.player_data : dict = conn.execute(f"SELECT * FROM PLAYERS WHERE player_id = {player_id}").fetchone()

    def display(self):
        for key, value in self.player_data.items():
            print(f"{key}: {value}")

    def return_player_copy(self):
        return self.player_data.copy()