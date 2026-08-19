# -*- coding: utf-8 -*-
"""
Списък с RSS източници за спортния бот.

Всеки източник има:
  - name:  кратко име на източника (показва се до заглавието)
  - url:   адрес на RSS канала
  - sport: към коя категория спада (виж SPORTS по-долу)
  - scope: 'all'     -> взима всички новини от този източник
           'bg_only' -> взима само новини, свързани с България/българи

Ако някой източник спре да работи, ботът просто го пропуска.
Можеш свободно да добавяш/махаш редове тук.
"""

# Емоджи + етикет за всяка категория (използва се в съобщението)
SPORTS = {
    "football":   "⚽ Футбол",
    "basketball": "🏀 Баскетбол",
    "tennis":     "🎾 Тенис",
    "volleyball": "🏐 Волейбол",
    "f1":         "🏎️ Формула 1",
    "athletics":  "🏃 Лека атлетика",
    "combat":     "🥊 Бойни спортове",
}

# Ключови думи, по които разпознаваме "българска" новина
BG_KEYWORDS = [
    "българ",
    "bulgar",
    "левски",
    "цска",
    "лудогорец",
    "ludogorets",
    "levski",
    "cska sofia",
]

FEEDS = [
    # ------------------------- ФУТБОЛ -------------------------
    {"name": "BBC Sport", "url": "https://feeds.bbci.co.uk/sport/football/rss.xml", "sport": "football", "scope": "all"},
    {"name": "Sky Sports", "url": "https://www.skysports.com/rss/12040", "sport": "football", "scope": "all"},
    {"name": "ESPN", "url": "https://www.espn.com/espn/rss/soccer/news", "sport": "football", "scope": "all"},
    {"name": "The Guardian", "url": "https://www.theguardian.com/football/rss", "sport": "football", "scope": "all"},
    {"name": "Marca", "url": "https://e00-marca.uecdn.es/rss/futbol/primera-division.xml", "sport": "football", "scope": "all"},
    {"name": "Foot Africa", "url": "https://foot-africa.com/en/feed/", "sport": "football", "scope": "all"},
    {"name": "Sportal", "url": "https://www.sportal.bg/rss.php?cat=1", "sport": "football", "scope": "all"},
    {"name": "Gong", "url": "https://gong.bg/rss", "sport": "football", "scope": "all"},

    # ------------------------- БАСКЕТБОЛ -------------------------
    {"name": "ESPN NBA", "url": "https://www.espn.com/espn/rss/nba/news", "sport": "basketball", "scope": "all"},
    {"name": "BasketNews", "url": "https://basketnews.com/rss.xml", "sport": "basketball", "scope": "all"},
    {"name": "BGbasket", "url": "https://bgbasket.com/feed/", "sport": "basketball", "scope": "all"},

    # ------------------------- ТЕНИС -------------------------
    {"name": "ESPN Tennis", "url": "https://www.espn.com/espn/rss/tennis/news", "sport": "tennis", "scope": "all"},
    {"name": "BGtennis", "url": "https://bgtennis.bg/feed/", "sport": "tennis", "scope": "all"},

    # ------------------------- ВОЛЕЙБОЛ -------------------------
    {"name": "BGvolleyball", "url": "https://bgvolleyball.com/feed/", "sport": "volleyball", "scope": "all"},
    {"name": "Worldofvolley", "url": "https://worldofvolley.com/feed", "sport": "volleyball", "scope": "all"},

    # ------------------------- ФОРМУЛА 1 -------------------------
    {"name": "ESPN F1", "url": "https://www.espn.com/espn/rss/rpm/news", "sport": "f1", "scope": "all"},
    {"name": "Motorsport", "url": "https://www.motorsport.com/rss/f1/news/", "sport": "f1", "scope": "all"},
    {"name": "The Race", "url": "https://the-race.com/feed/", "sport": "f1", "scope": "all"},

    # ------------------------- ЛЕКА АТЛЕТИКА (само българи) -------------------------
    {"name": "Sportal ЛА", "url": "https://www.sportal.bg/rss.php?cat=13", "sport": "athletics", "scope": "bg_only"},
    {"name": "World Athletics", "url": "https://worldathletics.org/feeds/news", "sport": "athletics", "scope": "bg_only"},

    # ------------------------- БОЙНИ СПОРТОВЕ (големи имена + българи) -------------------------
    {"name": "ESPN MMA", "url": "https://www.espn.com/espn/rss/mma/news", "sport": "combat", "scope": "all"},
    {"name": "BoxingScene", "url": "https://www.boxingscene.com/rss/news.xml", "sport": "combat", "scope": "all"},
]
