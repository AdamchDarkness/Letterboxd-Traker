# Letterboxd-Traker
A Discord bot that automatically posts new Letterboxd diary entries as threads in a forum channel — complete with film title, rating, poster, and review link.
> Perfect for film servers, cinephile communities, or personal film tracking groups!

---

## ✨ Features

- 🔍 Scrapes the latest diary entries from any Letterboxd user
- 🧠 Detects only new films logged *today*
- 🖼️ Retrieves high-quality posters using the TMDb API
- 💬 Creates a new thread in a Discord forum channel
- 🏷️ Adds a tag like `letterboxd` to organize posts
- ✅ Includes commands to manage tracked users live in Discord:
  - `!add <username>`
  - `!list`
  - `!remove <username>`
  - `!reload`

---

## ⚙️ Setup

### 1. Clone the repo
```bash
cd Letterboxd-Traker
```
### 2. Install dependencies
```python
  python3 -m venv env
  source env/bin/activate
  pip install -r requirements.txt
```
### 3. Create a config.ini file
At the root of your project:
```ini
[discord]
token = YOUR_DISCORD_BOT_TOKEN
forum_channel_id = YOUR_FORUM_CHANNEL_ID
tag_id = YOUR_TAG_ID

[tmdb]
api_key = YOUR_TMDB_API_KEY
```
### 4. Run the bot
```python
source env/bin/activate
python bot.py
```

---

## 🔐 Files

- bot.py → Main Discord bot logic
- watch.py → Letterboxd and TMDb logic + scheduler
- config.ini → Your API keys and channel config (do not commit this)
- usernames.json → Stores tracked usernames
- last_seen.json → Stores last posted films (used to avoid duplicates)

---

## 🛠️ Tools & Tech

- Python 3.12
- discord.py
- BeautifulSoup
- requests
- TMDb API

---

## 👤 Author
Made with ❤️ by Adam Charof | contact@adamcharof.com | adamchpro545@gmail.com
