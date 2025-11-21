import sqlite3
from modules.players import Player, Midfielder, Forward, Defender, Goalkeeper

# ----------------------------------------------------------
# Database Connection
# ----------------------------------------------------------

conn = sqlite3.connect(
    "/Users/levihauck/Documents/Fantasy-NWSL/Fantasy-NWSL/app/db/data/nwsl_fantasy.db"
)
conn.row_factory = sqlite3.Row

# ----------------------------------------------------------
# SQL Statements
# ----------------------------------------------------------

STARTERS_SQL = """
    SELECT * FROM players p
    JOIN fantasy_teams_rel r ON p.player_id = r.player_id
    JOIN fantasy_teams ft ON ft.team_id = r.f_team_id
    WHERE ft.team_id = ?
    AND r.is_sub = "False"
"""

SUBS_SQL = """
    SELECT * FROM players p
    JOIN fantasy_teams_rel r ON p.player_id = r.player_id
    JOIN fantasy_teams ft ON ft.team_id = r.f_team_id
    WHERE ft.team_id = ?
    AND r.is_sub = "True"
"""

# ----------------------------------------------------------
# Fantasy Team Class
# ----------------------------------------------------------

class FantasyTeam:
    def __init__(self, user_id):
        self.user_id = user_id

        # groups
        self.goalkeeper  = []
        self.defenders   = []
        self.midfielders = []
        self.forwards    = []
        self.substitutes = []

        # Load starters
        for row in conn.execute(STARTERS_SQL, (str(user_id),)):
            self._add_player(row, is_sub=False)

        # Load substitutes
        for row in conn.execute(SUBS_SQL, (str(user_id),)):
            self._add_player(row, is_sub=True)

    # --------------------------------------------------
    # Internal: Build player objects & categorize
    # --------------------------------------------------
    def _add_player(self, row, is_sub):
        pos = row["position"]

        # Correct player class
        if pos == "M":
            player = Midfielder(row)
        elif pos == "D":
            player = Defender(row)
        elif pos == "F":
            player = Forward(row)
        elif pos == "G":
            player = Goalkeeper(row)
        else:
            player = Player(row)

        # Sub players
        if is_sub:
            self.substitutes.append(player)
            return

        # Starters by position
        if pos == "G":
            self.goalkeeper.append(player)
        elif pos == "D":
            self.defenders.append(player)
        elif pos == "M":
            self.midfielders.append(player)
        elif pos == "F":
            self.forwards.append(player)

    # --------------------------------------------------
    # Visual print
    # --------------------------------------------------
    def display(self):
        for group in [
            self.goalkeeper,
            self.defenders,
            self.midfielders,
            self.forwards,
            self.substitutes,
        ]:
            for p in group:
                p.display()
    
    # takes a list of player_ids, creates a new team in the teams database
    def update_team(self, team: list, team_id, user_id):
        sql_stmt = f"""
        INSERT {team_id},{user_id} INTO fantasy_teams
        """
        conn.execute(sql_stmt)

        for pid in team:
            sql_stmt = f"""
            INSERT {team_id}, {pid} INTO fantasy_teams_rel
            """

            conn.execute(sql_stmt)

# ----------------------------------------------------------
# Convert Team → API Dictionary
# ----------------------------------------------------------

async def get_fantasy_team(user_id):
    team = FantasyTeam(user_id)
            # Convert player objects to dictionaries
    team_resp =  {
        str(user_id): {
            "goalkeeper":  [p for p in team.goalkeeper],
            "defenders":   [p for p in team.defenders],
            "midfielders": [p for p in team.midfielders],
            "forwards":    [p for p in team.forwards],
            "substitutes": [p for p in team.substitutes],
        }
    }
    return team_resp


async def save_fantasy_team(team, user_id, week_id):
    return (True, "Not implemented yet")

    # if team with same week_id exists in DB, remove old team from DB
    # otherwise, make a new team entry

    # insert new team into DB

