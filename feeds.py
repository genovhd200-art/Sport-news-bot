# -*- coding: utf-8 -*-
"""Списък с RSS източници за спортния бот."""

SPORTS = {
    "football":   "⚽ Футбол",
    "basketball": "🏀 Баскетбол",
    "tennis":     "🎾 Тенис",
    "volleyball": "🏐 Волейбол",
    "f1":         "🏎️ Формула 1",
    "athletics":  "🏃 Лека атлетика",
    "combat":     "🥊 Бойни спортове",
}

BG_KEYWORDS = [
    "българ", "bulgar", "левски", "цска",
    "лудогорец", "ludogorets", "levski", "cska sofia",
]

FEEDS = [
    # ------------------------- ФУТБОЛ -------------------------
    {"name": "BBC Sport", "url": "https://feeds.bbci.co.uk/sport/football/rss.xml", "sport": "football", "scope": "all"},
    {"name": "Sky Sports", "url": "https://www.skysports.com/rss/12040", "sport": "football", "scope": "all"},
    {"name": "ESPN", "url": "https://www.espn.com/espn/rss/soccer/news", "sport": "football", "scope": "all"},
    {"name": "The Guardian", "url": "https://www.theguardian.com/football/rss", "sport": "football", "scope": "all"},
    {"name": "Marca", "url": "https://e00-marca.uecdn.es/rss/futbol/primera-division.xml", "sport": "football", "scope": "all"},
    {"name": "Foot Africa", "url": "https://foot-africa.com/en/feed/", "sport": "football", "scope": "all"},
    {"name": "Gong", "url": "https://gong.bg/rss", "sport": "football", "scope": "all"},

    # ------------------------- БАСКЕТБОЛ -------------------------
    {"name": "BBC Basketball", "url": "https://feeds.bbci.co.uk/sport/basketball/rss.xml", "sport": "basketball", "scope": "all"},
    {"name": "CBS NBA", "url": "https://www.cbssports.com/rss/headlines/nba/", "sport": "basketball", "scope": "all"},
    {"name": "BGbasket", "url": "https://bgbasket.com/feed/", "sport": "basketball", "scope": "all"},

    # ------------------------- ТЕНИС -------------------------
    {"name": "BBC Tennis", "url": "https://feeds.bbci.co.uk/sport/tennis/rss.xml", "sport": "tennis", "scope": "all"},
    {"name": "ESPN Tennis", "url": "https://www.espn.com/espn/rss/tennis/news", "sport": "tennis", "scope": "all"},

    # ------------------------- ВОЛЕЙБОЛ -------------------------
    {"name": "WorldOfVolley", "url": "https://worldofvolley.com/feed", "sport": "volleyball", "scope": "all"},
    {"name": "BGvolleyball", "url": "https://bgvolleyball.com/feed/", "sport": "volleyball", "scope": "all"},

    # ------------------------- ФОРМУЛА 1 -------------------------
    {"name": "BBC F1", "url": "https://feeds.bbci.co.uk/sport/formula1/rss.xml", "sport": "f1", "scope": "all"},
    {"name": "The Race", "url": "https://the-race.com/feed/", "sport": "f1", "scope": "all"},
    {"name": "Motorsport", "url": "https://www.motorsport.com/rss/f1/news/", "sport": "f1", "scope": "all"},

    # ------------------------- ЛЕКА АТЛЕТИКА (само българи) -------------------------
    {"name": "BBC Athletics", "url": "https://feeds.bbci.co.uk/sport/athletics/rss.xml", "sport": "athletics", "scope": "bg_only"},

    # ------------------------- БОЙНИ СПОРТОВЕ (големи имена + българи) -------------------------
    {"name": "ESPN MMA", "url": "https://www.espn.com/espn/rss/mma/news", "sport": "combat", "scope": "all"},
    {"name": "BBC Boxing", "url": "https://feeds.bbci.co.uk/sport/boxing/rss.xml", "sport": "combat", "scope": "all"},
]
