import os
import json
import requests
import feedparser

TELEGRAM_TOKEN = os.environ["7868330519:AAGcAAQdrVXkviGRjo5vFgx-DEsWT-3Kgik"]
CHANNEL_ID = "-1002076804696"
FEED_URL = "https://techdaily.buzz/feed"
STATE_FILE = "last_post.json"

def load_last_post():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f).get("id")
    return None

def save_last_post(post_id):
    with open(STATE_FILE, "w") as f:
        json.dump({"id": post_id}, f)

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHANNEL_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()

def main():
    feed = feedparser.parse(FEED_URL)
    if not feed.entries:
        print("No entries found in feed.")
        return

    latest = feed.entries[0]
    post_id = latest.get("id") or latest.get("link")
    last_id = load_last_post()

    if post_id == last_id:
        print("No new posts.")
        return

    # Format message
    title = latest.get("title", "New Post")
    link = latest.get("link", "")
    summary = latest.get("summary", "")[:200] + "..." if latest.get("summary") else ""

    message = f"📰 <b>{title}</b>\n\n{summary}\n\n🔗 <a href='{link}'>Read more</a>"
    send_telegram_message(message)
    save_last_post(post_id)
    print(f"Posted: {title}")

if __name__ == "__main__":
    main()