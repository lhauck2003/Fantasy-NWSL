def calculate_fantasy_points(player_stats: dict, position: str) -> int:
    """
    Example scoring function
    """
    points = 0
    points += int(player_stats.get("goals_summary", 0)) * 5
    points += int(player_stats.get("assists_summary", 0)) * 3
    points += int(player_stats.get("minutes_summary", 0)) // 30
    if position == "GK":
        points += int(player_stats.get("saves_summary", 0))
    return points

class ScoringSystem:
    def calculate():
        pass

class MidfielderScoring(ScoringSystem):
    def __init__(self):
        self.points = 0

    def calculate(self, player_stats: dict):
        self.points += int(player_stats.get("goals_summary", 0)) * 5
        self.points += int(player_stats.get("assists_summary", 0)) * 3
        self.points += 2 if int(player_stats.get("minutes_summary", 0)) >= 60 else 1 if int(player_stats.get("minutes_summary", 0)) > 0 else 0
        self.points += int(player_stats.get("clean_sheets_summary", 0)) * 1
        return self.points

class ForwardScoring(ScoringSystem):
    def __init__(self):
        self.points = 0

    def calculate(self, player_stats: dict):
        self.points += int(player_stats.get("goals_summary", 0)) * 4
        self.points += int(player_stats.get("assists_summary", 0)) * 3
        self.points += 2 if int(player_stats.get("minutes_summary", 0)) >= 60 else 1 if int(player_stats.get("minutes_summary", 0)) > 0 else 0
        return self.points
    
class DefenderScoring(ScoringSystem):
    def __init__(self):
        self.points = 0

    def calculate(self, player_stats: dict):
        self.points += int(player_stats.get("goals_summary", 0)) * 6
        self.points += int(player_stats.get("assists_summary", 0)) * 3
        self.points += 2 if int(player_stats.get("minutes_summary", 0)) >= 60 else 1 if int(player_stats.get("minutes_summary", 0)) > 0 else 0
        self.points += int(player_stats.get("clean_sheets_summary", 0)) * 4
        return self.points

class GoalkeeperScoring(ScoringSystem):
    def __init__(self):
        self.points = 0

    def calculate(self, player_stats: dict):
        self.points += int(player_stats.get("goals_summary", 0)) * 7
        self.points += int(player_stats.get("assists_summary", 0)) * 4
        self.points += 2 if int(player_stats.get("minutes_summary", 0)) >= 60 else 1 if int(player_stats.get("minutes_summary", 0)) > 0 else 0
        self.points += int(player_stats.get("clean_sheets_summary", 0)) * 5
        self.points += int(player_stats.get("saves_summary", 0)) // 3
        return self.points
    
class BonusPointsCalculator(ScoringSystem):
    def __init__(self):
        self.points = 0

    def calculate(self, player_stats: dict):
        bonus_categories = ["defensive_contributions", "goals", "assists"]
        bonus_points_values = {
            "defensive_contributions": 1,
            "goals": 10,
            "assists": 6
        }
        for category in bonus_categories:
            self.points += int(player_stats.get(f"{category}_summary", 0)) * bonus_points_values[category]
        return self.points