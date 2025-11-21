import sqlite3
from modules.fantasy_team import FantasyTeam

conn = sqlite3.connect(
    "/Users/levihauck/Documents/Fantasy-NWSL/Fantasy-NWSL/app/db/data/nwsl_fantasy.db"
)
conn.row_factory = sqlite3.Row

class League:
    def __init__(self, league_id: int, name: str, ):
        self.league_id = league_id
        self.name = name
        self.teams = []

    def add_team(self, user_id: str):
        team = FantasyTeam(user_id)
        self.teams.append(team)

    def add_team(self, team_id: int):
        team = FantasyTeam(team_id)
        self.teams.append(team)

    def display_teams(self):
        for team in self.teams:
            team.display()


async def get_league_by_user_id(user_id: str) -> League:
    leagues: list  = conn.execute(
                    """
                    SELECT l.league_id, l.league_name, lr.team_id
                    FROM leagues l, league_relations lr, fantasy_teams ft
                    WHERE lr.user_id = ? AND lr.league_id = l.league_id AND ft.team_id = lr.team_id
                    """,
                    (user_id,)
                ).fetchall()
    for row in leagues:
        league = League(row["league_id"], row["league_name"])
        for team_id in leagues["team_id"]:
            league.add_team(team_id)
        return league