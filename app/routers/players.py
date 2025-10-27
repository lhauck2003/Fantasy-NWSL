## Code for displaying a catalog of all the players, ability to sort by a particular stat
import sqlite3

conn  = sqlite3.connect('app/data/nwsl_fantasy.db')

class Players(dict):

    def __init__(self, conn=conn):
        players = conn.execute("SELECT * FROM PLAYERS")

    def display(self):
        pass

class Player(dict):
    pass