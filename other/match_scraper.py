from bs4 import BeautifulSoup as BS, Comment
import cloudscraper
import time, random
import requests
import pandas as pd
import re
from time import sleep

URL = ["https://fbref.com/en/comps/182/stats/NWSL-Stats"]

BASE_URL = "https://fbref.com"

HEAEDERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/128.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Referer": "https://www.google.com/",
    "DNT": "1",
    "Upgrade-Insecure-Requests": "1",
}


POSITIONS = {
    "FW":"F",
    "LW":"F",
    "RW":"F",
    "AM":"M",
    "RM":"M",
    "LM":"M",
    "CM":"M",
    "DM":"M",
    "RB":"D",
    "LB":"D",
    "CB":"D",
    "FB":"D",
    "WB":"D",
    "GK":"G",
    "DF":"D",
    "MF":"M"
}



def polite_delay():
    time.sleep(random.uniform(0.5, 1.5))


def scrape_stats_to_csv(url, csv_file):
    print(f"Scraping match data from {url}")
    scraper = cloudscraper.create_scraper()  # creates a session that handles Cloudflare
    res = scraper.get(url, headers=HEAEDERS)
    res.raise_for_status()

    soup = BS(res.text, "html.parser")
    comments = soup.find_all(string=lambda text: isinstance(text, Comment))
    for comment in comments:
        if ("div_stats_standard" in comment):
            stat_table = BS(comment, "html.parser").find("div", {"class": "table_container",
                                              "id": "div_stats_standard"})
    

    stats = scrape_player_stats(stat_table)

    # scrape data into csvc
    df = pd.DataFrame(stats)
    df.to_csv(csv_file, mode='a', header=not pd.io.common.file_exists(csv_file), index=False)

    # print(player_stat_table[0:5])

def scrape_player_stats(table):
    all_stats = []
    rows = table.find("tbody").find_all("tr", recursive=False)

    for row in rows:
        # Find player cell
        player_cell = row.find("td", {"data-stat": "player"})
        if not player_cell:
            continue

        a = player_cell.find("a")
        if not a:
            continue

        player_link = a.get("href")
        player_id = player_link.split("/")[-2]

        stats = {"player_id": player_id}

        for td in row.find_all("td"):
            col = td.get("data-stat")
            val = td.text.strip()
            if (col == "position"):
                val = POSITIONS[val.split(",")[0]]
            stats[col] = val

        all_stats.append(stats)
    return all_stats

if __name__ == "__main__":
    date = input("Enter current date (MM-DD-YYYY): ")
    date = date.replace("/","-")

    for url in URL:
        stats_name = url.split("/")[-2]
        CSV = f"../app/db/data/{stats_name}-{date}.csv"
        scrape_stats_to_csv(url, CSV)
