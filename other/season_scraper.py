from bs4 import BeautifulSoup, Comment
import requests
import json
import time

from nwsl_match_stats_scraper import scrape_fbref_match_to_json  # your working match scraper

BASE_URL = "https://fbref.com"

def get_match_links(season_url):
    """Get all match report links from a FBref NWSL season schedule page."""
    response = requests.get(season_url)
    soup = BeautifulSoup(response.text, "html.parser")
    match_links = []

    # --- 1. Check commented tables ---
    comments = soup.find_all(string=lambda text: isinstance(text, Comment))
    for c in comments:
        comment_soup = BeautifulSoup(c, "html.parser")
        for tbody in comment_soup.find_all("tbody"):
            for row in tbody.find_all("tr"):
                link_tag = row.find("td", {"data-stat": "match_report"})
                if link_tag and link_tag.a:
                    href = link_tag.a.get("href")
                    match_links.append(BASE_URL + href)

    # --- 2. Check visible tables ---
    for tbody in soup.find_all("tbody"):
        for row in tbody.find_all("tr"):
            link_tag = row.find("td", {"data-stat": "match_report"})
            if link_tag and link_tag.a:
                href = link_tag.a.get("href")
                match_links.append(BASE_URL + href)

    # Remove duplicates
    match_links = list(dict.fromkeys(match_links))
    return match_links


def scrape_season_to_json(season_url, output_file, delay=2):
    """Scrape all matches in a season and save player stats to a JSON file."""
    all_players = []
    match_links = get_match_links(season_url)
    print(f"Found {len(match_links)} matches in the season.")

    for i, link in enumerate(match_links, 1):
        print(f"[{i}/{len(match_links)}] Scraping {link}")
        try:
            players = scrape_fbref_match_to_json(link)
            all_players.extend(players)
        except Exception as e:
            print(f"⚠️ Error scraping {link}: {e}")
        time.sleep(delay)

    with open(output_file, "w") as f:
        json.dump(all_players, f, indent=2)

    print(f"✅ Saved {len(all_players)} player-game records → {output_file}")


if __name__ == "__main__":
    season_url = "https://fbref.com/en/comps/182/schedule/NWSL-Scores-and-Fixtures"
    scrape_season_to_json(season_url, "nwsl_2025_season.json")
