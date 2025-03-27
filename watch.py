import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import os
import asyncio
from typing import Callable
import configparser


config = configparser.ConfigParser()
config.read("config.ini")

TMDB_API_KEY = config["tmdb"]["api_key"]

def get_tmdb_poster(title, year=None):
    url = "https://api.themoviedb.org/3/search/movie"
    params = {
        "api_key": TMDB_API_KEY,
        "query": title,
        "include_adult": False,
        "language": "fr-FR"
    }
    if year:
        params["year"] = year

    response = requests.get(url, params=params)
    if response.status_code != 200:
        return None

    data = response.json()
    results = data.get("results")
    if not results:
        return None

    poster_path = results[0].get("poster_path")
    if poster_path:
        return f"https://image.tmdb.org/t/p/w500{poster_path}"
    return None

def get_latest_diary_entry(username):
    url = f"https://letterboxd.com/{username}/films/diary/"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    entry = soup.find("tr", class_="diary-entry-row")
    if not entry:
        return None

    # Date
    day_str = entry.find("td", class_="td-day").text.strip()
    today = datetime.today()
    full_date_str = f"{day_str} {today.strftime('%b')} {today.year}"

    try:
        watched_date = datetime.strptime(full_date_str, "%d %b %Y").date()
    except ValueError:
        watched_date = None

    # Film
    film_link_tag = entry.find("td", class_="td-film-details").find("a")
    title = film_link_tag.text.strip()
    film_page = f"https://letterboxd.com{film_link_tag['href']}"
    rating_tag = entry.find("span", class_="rating")
    rating = rating_tag.text.strip() if rating_tag else "Pas de note"
    image_url = get_tmdb_poster(title)

    return {
        "username": username,
        "title": title,
        "date": str(watched_date) if watched_date else "Date inconnue",
        "rating": rating,
        "url": film_page,
        "image": image_url
    }

def load_last_seen():
    if os.path.exists("last_seen.json"):
        with open("last_seen.json", "r") as f:
            try:
                return json.load(f)
            except:
                return {}
    return {}

def save_last_seen(data):
    with open("last_seen.json", "w") as f:
        json.dump(data, f, indent=2)

async def watch_users(usernames, callback: Callable):
    last_seen = load_last_seen()
    print("📡 Surveillance Letterboxd démarrée...\n")

    while True:
        print("👁️ Watch_users lancé avec :", usernames)

        today = str(datetime.today().date())
        for username in usernames:
            entry = get_latest_diary_entry(username)
            if entry and entry["date"] == today:
                last_entry = last_seen.get(username)
                if not last_entry or last_entry["title"] != entry["title"]:
                    last_seen[username] = {
                        "title": entry["title"],
                        "date": today
                    }
                    save_last_seen(last_seen)
                    await callback(entry)
        await asyncio.sleep(5)
