# fills data base with data from CSVs
import sqlite3
import pandas as pd
PLAYER_MATCH_STATS_CSV = "/Users/levihauck/Documents/NWSL_fantasy/NWSL-Fantasy/app/db/data/player_match_stats.csv"
PLAYER_CSV = '/Users/levihauck/Documents/NWSL_fantasy/NWSL-Fantasy/app/db/data/players.csv'
TEAM_CSV = '/Users/levihauck/Documents/NWSL_fantasy/NWSL-Fantasy/app/db/data/teams.csv'
MATCH_CSV = '/Users/levihauck/Documents/NWSL_fantasy/NWSL-Fantasy/app/db/data/matches.csv'

DB = "/Users/levihauck/Documents/NWSL_fantasy/NWSL-Fantasy/app/db/data/nwsl_fantasy.db"

conn = sqlite3.connect(DB)
cursor = conn.cursor()  

# Load data to Player Match Stats Table (Match ID, Player ID, stats..., match points)
player_match_stats_df = pd.read_csv(PLAYER_MATCH_STATS_CSV)
player_match_stats_df.to_sql('player_match_stats', conn, if_exists='replace', index=False)

# test to find team names
teams = cursor.execute("SELECT DISTINCT team_id, team_name FROM player_match_stats;").fetchall()
teams_df = pd.DataFrame(teams)
print(teams_df)
teams_df.to_csv(TEAM_CSV, mode='a', header=not pd.io.common.file_exists(TEAM_CSV), index=False)


# Load data to Player Table (Player ID, Name, Team ID, Position, etc.)

# Load data to the Team Table (Team ID, Name, City)


# Load data to Match Table