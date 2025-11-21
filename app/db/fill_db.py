# fills data base with data from CSVs
import sqlite3
import pandas as pd
PLAYER_MATCH_STATS_CSV = "/Users/levihauck/Documents/Fantasy-NWSL/Fantasy-NWSL/app/db/data/player_match_stats.csv"
PLAYER_CSV = '/Users/levihauck/Documents/Fantasy-NWSL/Fantasy-NWSL/app/db/data/stats-11-17.csv'
TEAM_CSV = '/Users/levihauck/Documents/Fantasy-NWSL/Fantasy-NWSL/app/db/data/teams.csv'
MATCH_CSV = '/Users/levihauck/Documents/Fantasy-NWSL/Fantasy-NWSL/app/db/data/matches.csv'

DB = "/Users/levihauck/Documents/Fantasy-NWSL/Fantasy-NWSL/app/db/data/nwsl_fantasy.db"

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
players_df = pd.read_csv(PLAYER_CSV)
print(players_df)
players_df.to_sql('players', conn, if_exists='replace', index=False)

# Load data to the Team Table (Team ID, Name, City)


# Load data to Match Table

# Load testuser team
team_df = pd.DataFrame([{"user_id": "000001", "team_id": 1}])
print(team_df)
team_df.to_sql('fantasy_teams', conn, if_exists='replace', index=False)

team_players_df = pd.DataFrame([
    {"f_team_id":1, "player_id": "45419c74", "is_sub": "True"},
    {"f_team_id":1, "player_id": "e79fcfd2", "is_sub": "True"},
    {"f_team_id":1, "player_id": "51e267dc", "is_sub": "True"},
    {"f_team_id":1, "player_id": "06115ef0", "is_sub": "True"},
    {"f_team_id":1, "player_id": "53cef818", "is_sub": "False"},
    {"f_team_id":1, "player_id": "edb4b4b1", "is_sub": "False"},
    {"f_team_id":1, "player_id": "24a238da", "is_sub": "False"},
    {"f_team_id":1, "player_id": "e31c93ca", "is_sub": "False"},
    {"f_team_id":1, "player_id": "49d6d4a8", "is_sub": "False"},
    {"f_team_id":1, "player_id": "845abb1a", "is_sub": "False"},
    {"f_team_id":1, "player_id": "3a794757", "is_sub": "False"},
    {"f_team_id":1, "player_id": "9982f5c6", "is_sub": "False"},
    {"f_team_id":1, "player_id": "7824185a", "is_sub": "False"},
    {"f_team_id":1, "player_id": "81b39775", "is_sub": "False"},
    {"f_team_id":1, "player_id": "30f6344f", "is_sub": "False"},
])
print(team_players_df)
team_players_df.to_sql('fantasy_teams_rel', conn, if_exists='replace', index=False)

STARTERS_SQL = """
    SELECT * FROM players p
    JOIN fantasy_teams_rel r ON p.player_id = r.player_id
    JOIN fantasy_teams ft ON ft.team_id = r.f_team_id
    WHERE ft.user_id = ?
    AND r.is_sub = "False"
"""

rows = conn.execute(STARTERS_SQL, ("000001",)).fetchall()
df = pd.DataFrame(rows)
print(df)