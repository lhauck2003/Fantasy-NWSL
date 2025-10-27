from bs4 import BeautifulSoup
import requests
import json

# Map table id fragments → category label
CATEGORY_MAP = {
    "summary": "summary",
    "passing": "passing",
    "defense": "defense",
    "possession": "possession",
    "misc": "misc"
}

def scrape_fbref_match_to_json(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    players_dict = {}  # keyed by (player_id, team)

    for table in soup.find_all("table"):
        tbody = table.find("tbody")
        if not tbody:
            continue

        # Identify category (default "other")
        table_id = table.get("id", "")
        category = "other"
        for frag, cat in CATEGORY_MAP.items():
            if frag in table_id:
                category = cat
                break

        # Detect team name from caption
        caption = table.find("caption")
        if caption:
            team_name = caption.get_text(strip=True)
        elif "ACFC" in table_id:
            team_name = "Angel City FC"
        elif "SD" in table_id or "Wave" in table_id:
            team_name = "San Diego Wave"
        else:
            team_name = "Unknown"

        # Parse rows (each player)
        for row in tbody.find_all("tr"):
            player_data = {}
            th = row.find("th", {"data-stat": "player"})
            if not th:
                continue  # skip non-player rows

            player_name = th.get_text(strip=True)
            player_id = th.get("data-append-csv", player_name)  # fbref player ID if present

            # Collect stats for this category
            for cell in row.find_all("td"):
                stat_name = cell.get("data-stat")
                value = cell.get_text(strip=True)
                if stat_name:
                    player_data[f"{stat_name}_{category}"] = value

            # Build composite key (id + team ensures uniqueness)
            key = (player_id, team_name)

            if key not in players_dict:
                players_dict[key] = {
                    "player": player_name,
                    "player_id": player_id,
                    "team": team_name
                }

            # Merge this category's stats into the player dict
            players_dict[key].update(player_data)

    # Convert dict → list
    players_list = list(players_dict.values())
    return players_list


if __name__ == "__main__":
    url = "https://fbref.com/en/matches/0194ccbe/Angel-City-FC-San-Diego-Wave-March-16-2025-NWSL"
    players = scrape_fbref_match_to_json(url)

    # Pretty print
    print(json.dumps(players[:5], indent=2))  # show first 5 players

    # Save full JSON
    with open("match_player_stats.json", "w") as f:
        json.dump(players, f, indent=2)
