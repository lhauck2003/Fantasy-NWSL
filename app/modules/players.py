import sqlite3

# Connect with row_factory so rows behave like dicts!
conn = sqlite3.connect('./db/data/nwsl_fantasy.db')
conn.row_factory = sqlite3.Row


# ----------------------------------------------------------
# Base Player Class
# ----------------------------------------------------------
class Player(dict):
    def __init__(self, row: sqlite3.Row):
        super().__init__(row)   # convert row -> dict

    def display(self):
        for key, value in self.items():
            print(f"{key}: {value}")

    def calculate_points(self, week_id):
        """Overridden by subclasses."""
        return 0

    def update_price(self, diff: float):
        self["price"] = float(self["price"]) + diff
        

# ----------------------------------------------------------
# Subclasses for each position
# ----------------------------------------------------------
class Midfielder(Player):
    def calculate_points(self, week_id):
        player_id = self["id"]
        stats = conn.execute(
            "SELECT * FROM PLAYER_MATCH_STATS WHERE player_id=? AND week_id=?",
            (player_id, week_id)
        ).fetchone()

        if not stats:
            return 0

        points = (
            int(stats["goals_summary"]) * 5 +
            int(stats["assists_summary"]) * 3 +
            (2 if int(stats["minutes_summary"]) >= 60 else 1 if int(stats["minutes_summary"]) > 0 else 0) +
            int(stats.get("clean_sheets_summary", 0)) * 1
        )
        self["points"] = points
        return points


class Forward(Player):
    def calculate_points(self, week_id):
        player_id = self["id"]
        stats = conn.execute(
            "SELECT * FROM PLAYER_MATCH_STATS WHERE player_id=? AND week_id=?",
            (player_id, week_id)
        ).fetchone()

        if not stats:
            return 0

        points = (
            int(stats["goals_summary"]) * 4 +
            int(stats["assists_summary"]) * 3 +
            (2 if int(stats["minutes_summary"]) >= 60 else 1 if int(stats["minutes_summary"]) > 0 else 0)
        )
        self["points"] = points
        return points


class Defender(Player):
    def calculate_points(self, week_id):
        player_id = self["id"]
        stats = conn.execute(
            "SELECT * FROM PLAYER_MATCH_STATS WHERE player_id=? AND week_id=?",
            (player_id, week_id)
        ).fetchone()

        if not stats:
            return 0

        points = (
            int(stats["goals_summary"]) * 6 +
            int(stats["assists_summary"]) * 3 +
            (2 if int(stats["minutes_summary"]) >= 60 else 1 if int(stats["minutes_summary"]) > 0 else 0) +
            int(stats["clean_sheets_summary"]) * 4
        )
        self["points"] = points
        return points


class Goalkeeper(Player):
    def calculate_points(self, week_id):
        player_id = self["id"]
        stats = conn.execute(
            "SELECT * FROM PLAYER_MATCH_STATS WHERE player_id=? AND week_id=?",
            (player_id, week_id)
        ).fetchone()

        if not stats:
            return 0

        points = (
            int(stats["goals_summary"]) * 7 +
            int(stats["assists_summary"]) * 4 +
            (2 if int(stats["minutes_summary"]) >= 60 else 1 if int(stats["minutes_summary"]) > 0 else 0) +
            int(stats["clean_sheets_summary"]) * 5 +
            int(stats["saves_summary"]) // 3
        )
        self["points"] = points
        return points


# ----------------------------------------------------------
# Players — list of all Player objects
# ----------------------------------------------------------
class Players(list):
    def __init__(self):
        super().__init__()

        rows = conn.execute("SELECT * FROM PLAYERS").fetchall()

        for row in rows:
            pos = row["position"]
            if pos == "M":
                self.append(Midfielder(row))
            elif pos == "D":
                self.append(Defender(row))
            elif pos == "F":
                self.append(Forward(row))
            elif pos == "G":
                self.append(Goalkeeper(row))
            else:
                self.append(Player(row))

    def display(self):
        for p in self:
            p.display()
            print("-" * 80)


# ----------------------------------------------------------------
# Global players_db (like your original)
# ----------------------------------------------------------------
players_db = Players()
# convert list to {id: player} dict
players_db_dict = {player["player_id"]: player for player in players_db}
