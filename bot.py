# -*- coding: utf-8 -*-
"""
Спортен новинарски бот за Telegram.
Чете RSS от feeds.py, взима новите заглавия, маха повторенията
и ги праща в Telegram чат на български. Работи през GitHub Actions.

Употреба:
    python bot.py            # нормално пускане
    python bot.py --force    # прати веднага, без да гледа часа/интервала
    python bot.py --dry-run  # само покажи какво би пратил
    python bot.py --chatid   # покажи наличните chat ID-та
"""

import os
import re
import sys
import json
import html
import time
from datetime import datetime, timedelta, timezone

import requests
import feedparser

try:
    from zoneinfo import ZoneInfo
    SOFIA = ZoneInfo("Europe/Sofia")
except Exception:
    SOFIA = timezone(timedelta(hours=2))

from feeds import FEEDS, SPORTS, BG_KEYWORDS

# ------------------------- НАСТРОЙКИ -------------------------
STATE_FILE = "state.json"
OPEN_HOUR = 7
CLOSE_HOUR = 23
MIN_INTERVAL_MIN = 85
FIRST_RUN_LOOKBACK_H = 4
MAX_PER_SPORT = 4
MAX_TOTAL = 25
SEEN_LIMIT = 3000
FETCH_TIMEOUT = 15
TG_LIMIT = 3800

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; SportsNewsBot/1.0; +https://github.com)"
}


def load_state():
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        data = {}
    data.setdefault("seen", [])
    data.setdefault("last_post_iso", None)
    return data


def save_state(state):
    state["seen"] = state["seen"][-SEEN_LIMIT:]
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=0)


def is_bulgarian(text):
    t = (text or "").lower()
    return any(k in t for k in BG_KEYWORDS)


def entry_time(entry):
    for key in ("published_parsed", "updated_parsed"):
        tm = entry.get(key)
        if tm:
            try:
                return datetime.fromtimestamp(time.mktime(tm), tz=timezone.utc)
            except Exception:
                pass
    return None


def clean_title(title):
    title = html.unescape(title or "")
    title = re.sub(r"\s+", " ", title).strip()
    return title


def fetch_feed(feed):
    try:
        r = requests.get(feed["url"], headers=HEADERS, timeout=FETCH_TIMEOUT)
        r.raise_for_status()
        return feedparser.parse(r.content)
    except Exception as e:
        print(f"  ! Пропуснат източник {feed['name']} ({feed['url']}): {e}")
        return None


def collect_items(state, force=False):
    last_post_iso = state.get("last_post_iso")
    if last_post_iso:
        try:
            since = datetime.fromisoformat(last_post_iso)
        except Exception:
            since = datetime.now(timezone.utc) - timedelta(hours=FIRST_RUN_LOOKBACK_H)
    else:
        since = datetime.now(timezone.utc) - timedelta(hours=FIRST_RUN_LOOKBACK_H)

    seen = set(state["seen"])
    found = {}

    for feed in FEEDS:
        parsed = fetch_feed(feed)
        if not parsed:
            continue
        for entry in parsed.entries:
            link = entry.get("link") or entry.get("id")
            if not link or link in seen:
                continue
            title = clean_title(entry.get("title", ""))
            if not title:
                continue

            when = entry_time(entry)
            if when is not None and not force and when < since:
                continue

            if feed.get("scope") == "bg_only":
                blob = title + " " + clean_title(entry.get("summary", ""))
                if not is_bulgarian(blob):
                    continue

            item = {
                "sport": feed["sport"],
                "source": feed["name"],
                "title": title,
                "link": link,
                "when": when,
                "bg": is_bulgarian(title + " " + clean_title(entry.get("summary", ""))),
            }
            found.setdefault(feed["sport"], []).append(item)
            seen.add(link)

    for sport in found:
        found[sport].sort(
            key=lambda x: (x["bg"], x["when"] or datetime.min.replace(tzinfo=timezone.utc)),
            reverse=True,
        )
        found[sport] = found[sport][:MAX_PER_SPORT]

    return found


def build_messages(found):
    now_local = datetime.now(SOFIA)
    header = f"🏟️ <b>Спортни новини</b> · {now_local.strftime('%d.%m.%Y %H:%M')}"

    blocks = []
    total = 0
    for sport_key, sport_label in SPORTS.items():
        items = found.get(sport_key, [])
        if not items:
            continue
        lines = [f"\n<b>{sport_label}</b>"]
        for it in items:
            if total >= MAX_TOTAL:
                break
            flag = "🇧🇬 " if it["bg"] else ""
            title = html.escape(it["title"])
            lines.append(f'• {flag}<a href="{html.escape(it["link"])}">{title}</a> <i>({html.escape(it["source"])})</i>')
            total += 1
        if len(lines) > 1:
            blocks.append("\n".join(lines))

    if not blocks:
        return []

    body = header + "\n" + "\n".join(blocks)

    messages = []
    current = ""
    for line in body.split("\n"):
        if len(current) + len(line) + 1 > TG_LIMIT:
            messages.append(current)
            current = ""
        current += line + "\n"
    if current.strip():
        messages.append(current)
    return messages


def tg_api(token, method):
    return f"https://api.telegram.org/bot{token}/{method}"


def send_message(token, chat_id, text):
    resp = requests.post(
        tg_api(token, "sendMessage"),
        json={
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "HTML",
            "disable_web_page_preview": True,
        },
        timeout=30,
    )
    if not resp.ok:
        print(f"  ! Грешка при пращане: {resp.status_code} {resp.text}")
    resp.raise_for_status()
    return resp.json()


def show_chat_ids(token):
    r = requests.get(tg_api(token, "getUpdates"), timeout=30)
    data = r.json()
    print(json.dumps(data, ensure_ascii=False, indent=2))
    chats = {}
    for upd in data.get("result", []):
        msg = upd.get("message") or upd.get("channel_post") or {}
        chat = msg.get("chat")
        if chat:
            chats[chat["id"]] = chat.get("title") or chat.get("username") or chat.get("first_name", "")
    print("\n=== Намерени чатове ===")
    if not chats:
        print("Няма съобщения. Първо напиши нещо на бота в Telegram, после пусни пак.")
    for cid, name in chats.items():
        print(f"  CHAT_ID = {cid}   ({name})")


def main():
    args = sys.argv[1:]
    force = "--force" in args
    dry_run = "--dry-run" in args

    token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    chat_id = os.environ.get("TELEGRAM_CHAT_ID", "").strip()

    if "--chatid" in args:
        if not token:
            print("Липсва TELEGRAM_BOT_TOKEN.")
            sys.exit(1)
        show_chat_ids(token)
        return

    if not token or (not chat_id and not dry_run):
        print("Липсва TELEGRAM_BOT_TOKEN или TELEGRAM_CHAT_ID.")
        sys.exit(1)

    state = load_state()

    now_local = datetime.now(SOFIA)
    if not force and not (OPEN_HOUR <= now_local.hour < CLOSE_HOUR):
        print(f"Извън работно време ({now_local.strftime('%H:%M')}). Изход.")
        return

    if not force and state.get("last_post_iso"):
        try:
            last = datetime.fromisoformat(state["last_post_iso"])
            mins = (datetime.now(timezone.utc) - last).total_seconds() / 60
            if mins < MIN_INTERVAL_MIN:
                print(f"Само {mins:.0f} мин от последното съобщение. Изход.")
                return
        except Exception:
            pass

    print("Изтеглям източниците...")
    found = collect_items(state, force=force)
    messages = build_messages(found)

    if not messages:
        print("Няма нови новини този път.")
        return

    print(f"Ще пратя {len(messages)} съобщение(я).")
    if dry_run:
        for m in messages:
            print("-" * 60)
            print(m)
        return

    for m in messages:
        send_message(token, chat_id, m)
        time.sleep(1)

    all_links = [it["link"] for items in found.values() for it in items]
    state["seen"].extend(all_links)
    state["last_post_iso"] = datetime.now(timezone.utc).isoformat()
    save_state(state)
    print("Готово.")


if __name__ == "__main__":
    main()
