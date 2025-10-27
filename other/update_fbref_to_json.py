from bs4 import BeautifulSoup, Comment
import requests
import json
import time
import re
from nwsl_match_stats_scraper import scrape_fbref_match_to_json  # reuse your match scraper

BASE_URL = "https://fbref.com"

def get_match_links_by_gameweek(season_url, gameweek):
    """Get all match report links for a specific gameweek."""
    response = requests.get(season_url)
    soup = BeautifulSoup(response.text, "html.parser")
    match_links = []

    # --- check both commented and visible tables ---
    def extract_links(soup_like):
        links = []
        for tbody in soup_like.find_all("tbody"):
            for row in tbody.find_all("tr"):
                gw_cell = row.find("th", {"data-stat": "gameweek"})
                if not gw_cell:
                    continue
                gw_text = gw_cell.get_text(strip=True)
                if gw_text != str(gameweek):  # match only this gameweek
                    continue
                link_tag = row.find("td", {"data-stat": "match_report"})
                if link_tag and link_tag.a:
                    links.append(BASE_URL + link_tag.a.get("href"))
        return links

    # visible table
    match_links.extend(extract_links(soup))

    # commented-out table(s)
    comments = soup.find_all(string=lambda text: isinstance(text, Comment))
    for c in comments:
        comment_soup = BeautifulSoup(c, "html.parser")
        match_links.extend(extract_links(comment_soup))

    return list(dict.fromkeys(match_links))


def extract_match_id(url):
    """Extract match ID from a fbref match URL."""
    m = re.search(r"/matches/([a-f0-9]+)/", url)
    return m.group(1) if m else None


def update_fbref_to_json(season_url, gameweek, json_file, delay=1):
    """Update JSON file with new matches from a specific gameweek."""
    # Load existing data
    try:
        with open(json_file) as f:
            all_players = json.load(f)
    except FileNotFoundError:
        all_players = []

    # Collect existing match IDs
    existing_ids = {p.get("match_id") for p in all_players if "match_id" in p}

    # Get gameweek links
    links = get_match_links_by_gameweek(season_url, gameweek)
    print(f"Found {len(links)} matches in gameweek {gameweek}")

    new_count = 0
    for link in links:
        match_id = extract_match_id(link)
        if match_id in existing_ids:
            print(f"Skipping already scraped match {match_id}")
            continue

        print(f"Scraping new match {match_id} → {link}")
        try:
            players = scrape_fbref_match_to_json(link)
            # add match_id to each player record
            for p in players:
                p["match_id"] = match_id
                p["match_url"] = link
            all_players.extend(players)
            existing_ids.add(match_id)
            new_count += 1
        except Exception as e:
            print(f"⚠️ Error scraping {link}: {e}")
        time.sleep(delay)

    # Save back
    with open(json_file, "w") as f:
        json.dump(all_players, f, indent=2)

    print(f"✅ Added {new_count} new matches. Total records: {len(all_players)}")


if __name__ == "__main__":
    season_url = "https://fbref.com/en/comps/182/schedule/NWSL-Scores-and-Fixtures"
    update_fbref_to_json(season_url, gameweek=3, json_file="nwsl_2025_season.json")
    # display first few records for verification
    with open("nwsl_2025_season.json") as f:
        data = json.load(f)
        print(json.dumps(data[50:65], indent=2))  # print first 3 records for verification
        # find average clearances, interceptions, tackles if available from defenders
        defenders = [p for p in data if p.get("position_misc") == "CB" or p.get("position_misc") == "LB" or p.get("position_misc") == "RB" or p.get("position_misc") == "WB"]
        if defenders:
            avg_clearances = float(sum(float(p.get("clearances_defense", 0)) for p in defenders) / len(defenders))
            avg_interceptions = float(sum(float(p.get("interceptions_summary", 0)) for p in defenders) / len(defenders))
            avg_tackles = float(sum(float(p.get("tackles_summary", 0)) for p in defenders) / len(defenders))
            avg_ball_recoveries = float(sum(float(p.get("ball_recoveries_misc", 0)) for p in defenders) / len(defenders))
            print(f"Avg Clearances (D): {avg_clearances:.2f}, Avg Interceptions (D): {avg_interceptions:.2f}, Avg Tackles (D): {avg_tackles:.2f}, Avg Ball Recoveries (D): {avg_ball_recoveries:.2f}")
        # get all positions
        positions = set(p.get("position_misc") for p in data if "position_misc" in p)
        print(f"Positions found: {positions}")