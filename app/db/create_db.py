# SQL Database Creation Script
import sqlite3

conn = sqlite3.connect('app/db/data/nwsl_fantasy.db')
cursor = conn.cursor()

# Player Table (Player ID, Name, Team ID, Position, etc.)
player_table_sql = """
CREATE TABLE IF NOT EXISTS players (
    player TEXT,
    team_id TEXT,
    team_name TEXT,
    shirtnumber INT,
    nationality TEXT,
    position TEXT NOT NULL CHECK (position IN ('G', 'D', 'M', 'F')),
    age INT,
    toal_minutes INT,
    total_goals INT,
    total_assists INT,
    total_pens_made INT,
    total_pens_att INT,
    total_shots INT,
    total_shots_on_target INT,
    total_cards_yellow INT,
    total_cards_red INT,
    total_touches INT,
    total_tackles INT, 
    total_interceptions INT,
    total_blocks INT,
    total_xg FLOAT,
    total_npxg FLOAT,
    total_xg_assist FLOAT,
    total_sca INT,
    total_gca INT,
    total_passes_completed INT,
    total_passes INT,
    passes_pct FLOAT,
    total_progressive_passes INT,
    total_carries INT,
    total_progressive_carries INT,
    total_take_ons INT,
    total_take_ons_won INT,
    player_id TEXT,
    price FLOAT,
    owners_count INT,
    PRIMARY KEY (player_id),
    FOREIGN KEY (player_id) REFERENCES players(player_id)
);
"""

# Team Table (Team ID, Team Name, etc.)
team_table_sql = """
CREATE TABLE IF NOT EXISTS teams (
    team_id TEXT PRIMARY KEY,
    team_name TEXT,
    team_location TEXT
);
"""

# Match Table (Match ID, Date, Home Team, Away Team, Score)
match_table_sql = """
CREATE TABLE IF NOT EXISTS matches (
    match_id TEXT PRIMARY KEY,
    week_id TEXT,
    match_date TEXT,
    home_team_id TEXT, 
    away_team_id TEXT,
    home_score INTEGER,
    away_score INTEGER,
    FOREIGN KEY (home_team_id) REFERENCES teams(team_id),
    FOREIGN KEY (away_team_id) REFERENCES teams(team_id),
    FOREIGN KEY (week_id) REFERENCES match_weeks(week_id)
);  
"""

# Player Match Stats Table (Match ID, Player ID, stats..., match points)
player_match_stats_table_sql = """
CREATE TABLE IF NOT EXISTS player_match_stats (
    player TEXT,
    team_id TEXT,
    team_name TEXT,
    match_date DATE,
    shirtnumber INT,
    nationality TEXT,
    position TEXT NOT NULL CHECK (position IN ('G', 'D', 'M', 'F')),
    age INT,
    minutes INT,
    goals INT,
    assists INT,
    pens_made INT,
    pens_att INT,
    shots INT,
    shots_on_target INT,
    cards_yellow INT,
    cards_red INT,
    touches INT,
    tackles INT, 
    interceptions INT,
    blocks INT,
    xg FLOAT,
    npxg FLOAT,
    xg_assist FLOAT,
    sca INT,
    gca INT,
    passes_completed INT,
    passes INT,
    passes_pct FLOAT,
    progressive_passes INT,
    carries INT,
    progressive_carries INT,
    take_ons INT,
    take_ons_won INT,
    player_id TEXT,
    PRIMARY KEY (match_id, player_id),
    FOREIGN KEY (player_id) REFERENCES players(player_id)
);  
"""

# User Table (User ID, Username, Password Hash)
user_table_sql = """
CREATE TABLE IF NOT EXISTS users (
    user_id TEXT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    PRIMARY KEY (username, password_hash)
);
"""

match_week_table_sql = """
CREATE TABLE IF NOT EXISTS match_weeks (
    week_id TEXT PRIMARY KEY,
    start_date TEXT,
    end_date TEXT
);
"""

# Schedule Table (Match ID, Home Team ID, Away Team ID)
# relational table between matches and teams
schedule_table_sql = """
CREATE TABLE IF NOT EXISTS schedule (
    match_id TEXT,
    h_team_id TEXT,
    a_team_id TEXT,
    PRIMARY KEY (match_id, h_team_id, a_team_id),
    FOREIGN KEY (match_id) REFERENCES matches(match_id),
    FOREIGN KEY (h_team_id) REFERENCES teams(team_id),
    FOREIGN KEY (a_team_id) REFERENCES teams(team_id)
);
"""

# Fantasy Team Table (team_id = User ID, Player IDs, Total Points)
fantasy_team_table_sql = """
CREATE TABLE IF NOT EXISTS fantasy_teams (
    team_id TEXT,
    week_id TEXT,
    PRIMARY KEY (team_id, week_id),
    FOREIGN KEY (team_id) REFERENCES users(user_id),
    FOREIGN KEY (week_id) REFERENCES match_weeks(week_id)
);
"""

# Fantasy Account Table (user_id, balance, total_points)
# holds user account information for fantasy league
fantasy_account_table_sql = """
CREATE TABLEL IF NOT EXISTS fantasy_accounts (
    user_id TEXT,
    team_id TEXT,
    balance FLOAT,
    total_points INT,
    PRIMARY KEY (user_id, team_id),
    FOREIGN KEY (user_id) REFERENCES user(user_id),
    FOREIGN KEY (team_id) REFERENCES fantasy_teams(team_id)
);
"""

# Fantasy Team Relational Table (team_id, player_id, is_sub)
# relational table between fantasy teams and players in the team
fantasy_team_rel_sql = """
CREATE TABLE IF NOT EXISTS fantasy_teams_rel(
    f_team_id TEXT,
    player_id TEXT,
    is_sub TEXT,
    PRIMARY KEY (f_team_id, player_id),
    FOREIGN KEY (f_team_id) REFERENCES fantasy_teams(team_id),
    FOREIGN KEY (player_id) REFERENCES players(player_id)
);
"""

league_table_sql = """
CREATE TABLE IF NOT EXISTS leagues (
    league_id TEXT PRIMARY KEY,
    league_name TEXT,
    owner_id TEXT,
    FOREIGN KEY (owner_id) REFERENCES users(user_id)
);
"""

league_rel_sql = """
CREATE TABLE IF NOT EXISTS league_rel (
    league_id TEXT,
    team_id TEXT,
    PRIMARY KEY (league_id, team_id),
    FOREIGN KEY (league_id) REFERENCES leagues(league_id),
    FOREIGN KEY (team_id) REFERENCES fantasy_teams(team_id)
);
"""


# Execute table creation statements
cursor.execute(player_table_sql)
cursor.execute(team_table_sql)
cursor.execute(match_table_sql)
cursor.execute(player_match_stats_table_sql)
cursor.execute(user_table_sql)
cursor.execute(match_week_table_sql)
cursor.execute(fantasy_team_table_sql)
cursor.execute(fantasy_team_rel_sql)
cursor.execute(league_table_sql)
cursor.execute(league_rel_sql)
cursor.execute(schedule_table_sql)
cursor.execute(fantasy_account_table_sql)