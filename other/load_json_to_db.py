# db_loader.py
import json
import re
import time
from datetime import datetime
import mysql.connector

# ---------- CONFIG ----------
DB_CONF = {
    "user": "your_mysql_user",
    "password": "your_mysql_password",
    "host": "127.0.0.1",
    "database": "nwsl_db",
    "port": 3306,
}
SEASON_JSON = "nwsl_2025_season.json"   # produced by your scraper
DELAY = 0.01
# ----------------------------

# position normalization mapping (map common strings to code)
POS_MAP = {
    "LW": "F", "RW": "F", "FW": "F", "AM": "F",    # user said AM -> forward (AM in parentheses)
    "DM": "M", "AM": "M", "CM": "M", "LM": "M", "RM": "M",
    "WB": "D", "CB": "D", "RB": "D", "LB": "D",
    "GK": "G"
}

# Fantasy scoring rules (tweak as needed)
SCORING = {
    "appearance_60": 2,    # >=60 min
    "appearance_sub": 1,   # <60 and >0
    "goal_FWD": 4,
    "goal_MID": 5,
    "goal_DEF": 6,
    "goal_GK": 6,
    "assist": 3,
    "clean_sheet_DEF_GK": 4,
    "yellow": -1,
    "red": -3,
    "saves_per_3": 1,      # 1 point per 3 saves for GK
    "pen_save": 5,
    "own_goal": -2
}

# ---------- utility helpers ----------
def connect():
    return mysql.connector.connect(**DB_CONF)

def ensure_tables_exist(conn):
    """Create tables if not already created. Paste the CREATE TABLE SQL above here (or run SQL file)."""
    # For brevity, assume you already created tables manually via SQL.
    # If you want this script to create tables programmatically, run the CREATE TABLE DDLs here.
    pass

def parse_int_safe(x):
    try:
        return int(x) if x is not None and x != "" else 0
    except:
        try:
            return int(float(x))
        except:
            return 0

def extract_match_id_from_url(url):
    m = re.search(r"/matches/([a-f0-9]+)/", url)
    return m.group(1) if m else None

# ---------- upsert helpers ----------
def upsert_team(cursor, team_name, fbref_slug=None):
    # try find by fbref_slug then name
    cursor.execute("SELECT team_id FROM team WHERE fbref_team_slug = %s", (fbref_slug,))
    r = cursor.fetchone()
    if r:
        return r[0]
    cursor.execute("SELECT team_id FROM team WHERE name = %s", (team_name,))
    r = cursor.fetchone()
    if r:
        return r[0]
    cursor.execute(
        "INSERT INTO team (fbref_team_slug, name) VALUES (%s, %s)",
        (fbref_slug, team_name)
    )
    return cursor.lastrowid

def upsert_player(cursor, player_id, name, team_id=None, primary_position=None):
    cursor.execute("SELECT player_id FROM player WHERE player_id = %s", (player_id,))
    if cursor.fetchone():
        # update team or name if changed
        cursor.execute(
            "UPDATE player SET name=%s, team_id=%s, primary_position=%s WHERE player_id=%s",
            (name, team_id, primary_position, player_id)
        )
        return player_id
    cursor.execute(
        "INSERT INTO player (player_id, name, team_id, primary_position) VALUES (%s,%s,%s,%s)",
        (player_id, name, team_id, primary_position)
    )
    return player_id

def upsert_game(cursor, game_id, match_url=None, date=None, kickoff=None, home_team_id=None, away_team_id=None,
                home_score=None, away_score=None, venue=None, attendance=None, referee=None):
    cursor.execute("SELECT game_id FROM game WHERE game_id = %s", (game_id,))
    if cursor.fetchone():
        cursor.execute("""
            UPDATE game SET match_url=%s, date=%s, kickoff=%s, home_team_id=%s, away_team_id=%s,
                            home_score=%s, away_score=%s, venue=%s, attendance=%s, referee=%s
            WHERE game_id = %s
        """, (match_url, date, kickoff, home_team_id, away_team_id, home_score, away_score, venue, attendance, referee, game_id))
        return game_id
    cursor.execute("""
        INSERT INTO game (game_id, match_url, date, kickoff, home_team_id, away_team_id,
                          home_score, away_score, venue, attendance, referee)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (game_id, match_url, date, kickoff, home_team_id, away_team_id, home_score, away_score, venue, attendance, referee))
    return game_id

def upsert_player_game_stat(cursor, p):
    """
    p is a dict with keys:
      player_id, match_id/game_id, team (team name or id), and stat keys from json
    We'll normalize keys and upsert into player_game_stat.
    """
    player_id = p.get("player_id")
    game_id = p.get("match_id") or p.get("game_id")
    team_name = p.get("team")
    # try find team_id
    cursor.execute("SELECT team_id FROM team WHERE name = %s", (team_name,))
    r = cursor.fetchone()
    team_id = r[0] if r else None

    minutes = parse_int_safe(p.get("minutes_summary") or p.get("minutes") or p.get("min"))
    goals = parse_int_safe(p.get("goals_summary") or p.get("goals"))
    assists = parse_int_safe(p.get("assists_summary") or p.get("assists"))
    pens_made = parse_int_safe(p.get("pens_made_summary") or p.get("pens_made"))
    pens_att = parse_int_safe(p.get("pens_att_summary") or p.get("pens_att"))
    yellow = parse_int_safe(p.get("cards_yellow_summary") or p.get("yellow_cards"))
    red = parse_int_safe(p.get("cards_red_summary") or p.get("red_cards"))
    saves = parse_int_safe(p.get("saves_summary") or p.get("saves"))
    # penalty_saves detection - placeholder: if fbref has "penalty_saves" or "penalty_saved"
    pen_saves = parse_int_safe(p.get("penalty_saves") or p.get("pens_saved") or 0)

    tackles = parse_int_safe(p.get("tackles_summary") or p.get("tackles"))
    interceptions = parse_int_safe(p.get("interceptions_summary") or p.get("interceptions"))
    clearances = parse_int_safe(p.get("clearances_defense") or p.get("clearances"))
    ball_recoveries = parse_int_safe(p.get("ball_recoveries_misc") or p.get("ball_recoveries") or 0)
    own_goals = parse_int_safe(p.get("own_goals_misc") or p.get("own_goals") or 0)

    defensive_contrib = tackles + interceptions + clearances + ball_recoveries

    # Upsert into player_game_stat
    # If record exists update, else insert
    cursor.execute("SELECT id FROM player_game_stat WHERE player_id=%s AND game_id=%s", (player_id, game_id))
    r = cursor.fetchone()
    if r:
        cursor.execute("""
            UPDATE player_game_stat
            SET team_id=%s, minutes=%s, goals=%s, assists=%s, pens_made=%s, pens_att=%s,
                yellow_cards=%s, red_cards=%s, saves=%s, penalty_saves=%s,
                tackles=%s, interceptions=%s, clearances=%s, ball_recoveries=%s,
                own_goals=%s, defensive_contrib=%s
            WHERE player_id=%s AND game_id=%s
        """, (team_id, minutes, goals, assists, pens_made, pens_att,
              yellow, red, saves, pen_saves,
              tackles, interceptions, clearances, ball_recoveries,
              own_goals, defensive_contrib, player_id, game_id))
    else:
        cursor.execute("""
            INSERT INTO player_game_stat
            (player_id, game_id, team_id, minutes, goals, assists, pens_made, pens_att,
             yellow_cards, red_cards, saves, penalty_saves, tackles, interceptions, clearances, ball_recoveries,
             own_goals, defensive_contrib)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (player_id, game_id, team_id, minutes, goals, assists, pens_made, pens_att,
              yellow, red, saves, pen_saves, tackles, interceptions, clearances, ball_recoveries,
              own_goals, defensive_contrib))
    return True

# ---------- compute fantasy points ----------
def compute_points_for_row(row, pos_code):
    """row: dict of stats for a single player-game. pos_code is one of 'F','M','D','G'"""
    points = 0
    minutes = parse_int_safe(row.get("minutes") or row.get("minutes_summary") or 0)
    # appearance
    if minutes >= 60:
        points += SCORING["appearance_60"]
    elif minutes > 0:
        points += SCORING["appearance_sub"]

    goals = parse_int_safe(row.get("goals") or row.get("goals_summary") or 0)
    if pos_code == "F":
        points += goals * SCORING["goal_FWD"]
    elif pos_code == "M":
        points += goals * SCORING["goal_MID"]
    elif pos_code == "D":
        points += goals * SCORING["goal_DEF"]
    elif pos_code == "G":
        points += goals * SCORING["goal_GK"]

    assists = parse_int_safe(row.get("assists") or row.get("assists_summary") or 0)
    points += assists * SCORING["assist"]

    # clean sheet: need goals_against for team in that game; here assume caller supplies 'team_goals_against' if desired
    # For now skip automatic clean-sheet until game data exists.

    if (row.get("cards_yellow") == "1") or (row.get("cards_yellow_summary") == "1"):
        points += SCORING["yellow"]
    if (row.get("cards_red") == "1") or (row.get("cards_red_summary") == "1"):
        points += SCORING["red"]

    if pos_code == "G":
        saves = parse_int_safe(row.get("saves") or row.get("saves_summary") or 0)
        points += (saves // 3) * SCORING["saves_per_3"]
        pen_saves = parse_int_safe(row.get("penalty_saves") or row.get("pens_saved") or 0)
        points += pen_saves * SCORING["pen_save"]

    own_goals = parse_int_safe(row.get("own_goals") or row.get("own_goals_misc") or 0)
    points += own_goals * SCORING["own_goal"]

    return points

# ---------- main ETL ----------
def load_json_to_db(json_file):
    conn = connect()
    cursor = conn.cursor()
    ensure_tables_exist(conn)  # optionally create tables

    # load json
    with open(json_file) as f:
        data = json.load(f)

    # existing games and players cache
    cursor.execute("SELECT game_id FROM game")
    existing_games = {r[0] for r in cursor.fetchall()}

    cursor.execute("SELECT player_id FROM player")
    existing_players = {r[0] for r in cursor.fetchall()}

    inserted_games = 0
    inserted_players = 0
    inserted_stats = 0

    for rec in data:
        # rec contains keys like: player, player_id, team, match_id, and many stats with suffixes
        # extract identifiers
        player_id = rec.get("player_id") or rec.get("id") or rec.get("playerId") or rec.get("player")
        if not player_id:
            # fallback generate id from name
            player_id = re.sub(r"\s+", "_", rec.get("player","unknown")).lower()

        player_name = rec.get("player")
        team_name = rec.get("team")
        match_id = rec.get("match_id") or extract_match_id_from_url(rec.get("match_url","")) or rec.get("game_id")

        if not match_id:
            continue  # skip malformed

        # upsert team
        team_id = None
        if team_name:
            cursor.execute("SELECT team_id FROM team WHERE name=%s", (team_name,))
            r = cursor.fetchone()
            if r:
                team_id = r[0]
            else:
                cursor.execute("INSERT INTO team (name) VALUES (%s)", (team_name,))
                team_id = cursor.lastrowid

        # upsert game (minimally)
        if match_id not in existing_games:
            # we may not have full info for home/away; insert placeholder
            cursor.execute("INSERT INTO game (game_id, match_url) VALUES (%s,%s)", (match_id, rec.get("match_url")))
            existing_games.add(match_id)
            inserted_games += 1

        # upsert player
        # Map a primary_position if present in rec (try to find any position-like keys)
        # some FBref tables have 'position' or 'pos'
        pos_raw = rec.get("position") or rec.get("pos") or rec.get("position_summary")
        pos_code = None
        if pos_raw:
            pos_candidate = pos_raw.strip().upper()
            # normalize to one of POS_MAP keys
            if pos_candidate in POS_MAP:
                pos_code = POS_MAP[pos_candidate]
            else:
                # fallback - check beginning
                for k in POS_MAP:
                    if pos_candidate.startswith(k):
                        pos_code = POS_MAP[k]
                        break
        # insert or update player
        if player_id not in existing_players:
            cursor.execute("INSERT INTO player (player_id, name, team_id, primary_position) VALUES (%s,%s,%s,%s)",
                           (player_id, player_name, team_id, pos_code))
            existing_players.add(player_id)
            inserted_players += 1
        else:
            cursor.execute("UPDATE player SET name=%s, team_id=%s, primary_position=%s WHERE player_id=%s",
                           (player_name, team_id, pos_code, player_id))

        # upsert player_game_stat
        # Normalize rec keys into the keys expected by upsert_player_game_stat
        # Our upsert function expects fields like minutes_summary, goals_summary etc if present
        # Ensure 'match_id' is present
        rec['match_id'] = match_id
        rec['team'] = team_name
        upsert_player_game_stat(cursor, rec)
        inserted_stats += 1

        # commit periodically
        if (inserted_stats % 200) == 0:
            conn.commit()
            print(f"Committed {inserted_stats} stats...")

        time.sleep(DELAY)

    conn.commit()
    print(f"Inserted games: {inserted_games}, players: {inserted_players}, stats rows processed: {inserted_stats}")

    # compute fantasy weekly points:
    compute_and_store_weekly_points(conn, cursor)

    cursor.close()
    conn.close()

def compute_and_store_weekly_points(conn, cursor):
    """
    This routine:
      - determines gameweek membership for games (requires gameweek table or infers by date),
      - aggregates points per player per gameweek and upserts fantasy_weekly_points and fantasy_player_total.
    For simplicity, we'll infer gameweek by the game's date's week number (ISO week). If you maintain a gameweek table, replace logic.
    """
    # get all player_game_stat rows joined with game date and player position
    cursor.execute("""
        SELECT pgs.player_id, pgs.game_id, g.date, p.primary_position,
               pgs.minutes, pgs.goals, pgs.assists, pgs.pens_made, pgs.pens_att,
               pgs.yellow_cards, pgs.red_cards, pgs.saves, pgs.penalty_saves, pgs.own_goals
        FROM player_game_stat pgs
        JOIN player p ON pgs.player_id = p.player_id
        LEFT JOIN game g ON pgs.game_id = g.game_id
    """)
    rows = cursor.fetchall()
    # columns index mapping
    # We'll create a mapping using cursor.column_names if needed; for now assume order above
    # Build a mapping: gameweek_key -> id (create simple gameweeks table by ISO week)
    gw_map = {}  # ("YYYY-WW") -> gameweek_id
    # prefetch gameweek table
    cursor.execute("SELECT gameweek_id, gw_label FROM gameweek")
    for r in cursor.fetchall():
        gw_map[r[1]] = r[0]

    points_agg = {}  # (player_id, gameweek_label) -> sum_points

    for r in rows:
        player_id = r[0]
        game_id = r[1]
        date_obj = r[2]
        pos = r[3] or "F"
        minutes = r[4] or 0
        goals = r[5] or 0
        assists = r[6] or 0
        pens_made = r[7] or 0
        pens_att = r[8] or 0
        yellow = r[9] or 0
        red = r[10] or 0
        saves = r[11] or 0
        pen_saves = r[12] or 0
        own_goals = r[13] or 0

        # compute pos_code from pos if pos is like 'LW' or 'FWD'
        pos_upper = (pos or "").upper()
        pos_code = POS_MAP.get(pos_upper, pos_upper[0] if pos_upper else "F")

        # build a simple row dict
        row_dict = {
            "minutes": minutes,
            "goals": goals,
            "assists": assists,
            "pens_made": pens_made,
            "pens_att": pens_att,
            "cards_yellow": yellow,
            "cards_red": red,
            "saves": saves,
            "penalty_saves": pen_saves,
            "own_goals": own_goals
        }

        points = compute_points_for_row(row_dict, pos_code)

        # assign gameweek label by date: "YYYY-WW" using ISO week
        if isinstance(date_obj, datetime):
            iso_year, iso_week, _ = date_obj.isocalendar()
            gw_label = f"{iso_year}-W{iso_week:02d}"
        elif isinstance(date_obj, str):
            try:
                d = datetime.fromisoformat(date_obj)
                iso_year, iso_week, _ = d.isocalendar()
                gw_label = f"{iso_year}-W{iso_week:02d}"
            except:
                gw_label = "unknown"
        else:
            gw_label = "unknown"

        # ensure gameweek exists
        if gw_label not in gw_map:
            cursor.execute("INSERT INTO gameweek (gw_label) VALUES (%s)", (gw_label,))
            gw_id = cursor.lastrowid
            gw_map[gw_label] = gw_id
            conn.commit()
        else:
            gw_id = gw_map[gw_label]

        key = (player_id, gw_id)
        points_agg[key] = points_agg.get(key, 0) + points

    # upsert into fantasy_weekly_points and update fantasy_player_total
    for (player_id, gw_id), pts in points_agg.items():
        cursor.execute("SELECT points FROM fantasy_weekly_points WHERE player_id=%s AND gameweek_id=%s", (player_id, gw_id))
        if cursor.fetchone():
            cursor.execute("UPDATE fantasy_weekly_points SET points=%s WHERE player_id=%s AND gameweek_id=%s", (pts, player_id, gw_id))
        else:
            cursor.execute("INSERT INTO fantasy_weekly_points (player_id, gameweek_id, points) VALUES (%s,%s,%s)", (player_id, gw_id, pts))

        # update total
        cursor.execute("SELECT total_points FROM fantasy_player_total WHERE player_id=%s", (player_id,))
        r = cursor.fetchone()
        if r:
            # recompute total by summing fantasy_weekly_points (robust)
            cursor.execute("SELECT COALESCE(SUM(points),0) FROM fantasy_weekly_points WHERE player_id=%s", (player_id,))
            total = cursor.fetchone()[0]
            cursor.execute("UPDATE fantasy_player_total SET total_points=%s WHERE player_id=%s", (total, player_id))
        else:
            # insert total
            cursor.execute("SELECT COALESCE(SUM(points),0) FROM fantasy_weekly_points WHERE player_id=%s", (player_id,))
            total = cursor.fetchone()[0]
            cursor.execute("INSERT INTO fantasy_player_total (player_id, total_points) VALUES (%s,%s)", (player_id, total))

    conn.commit()
    print("Fantasy weekly points and totals updated.")

# ---------- run ----------
if __name__ == "__main__":
    load_json_to_db(SEASON_JSON)
