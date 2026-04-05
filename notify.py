import os
import json
import requests
import feedparser
from bs4 import BeautifulSoup

TELEGRAM_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]

CHANNELS = ["@techdaily_buzz", "@tech_empire"]
ADMIN_CHAT = "YOUR_NUMERIC_USER_ID_HERE"  # Replace with your ID from @userinfobot

FEED_URL = "https://techdaily.buzz/feed.php"
STATE_FILE = "last_post.json"

def load_last_post():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f).get("url")
    return None

def save_last_post(post_url):
    with open(STATE_FILE, "w") as f:
        json.dump({"url": post_url}, f)

def get_latest_post():
    feed = feedparser.parse(FEED_URL)
    if not feed.entries:
        print("No entries found in feed.")
        return None, None, None

    latest = feed.entries[0]
    title = latest.get("title", "New Post")
    link = latest.get("link", "")
    description = latest.get("summary", "")
    if len(description) > 200:
        description = description[:200].rsplit(" ", 1)[0] + "..."
    return title, link, description

def get_post_tags(post_url):
    """Scrape tags from the individual post page."""
    try:
        response = requests.get(post_url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        tags = []
        for a in soup.find_all("a", href=True):
            if "/tag/" in a["href"]:
                tag_text = a.get_text(strip=True)
                if tag_text and tag_text not in tags:
                    tags.append(tag_text)
        return tags
    except Exception as e:
        print(f"Could not fetch tags: {e}")
        return []

def format_tags(tags):
    if not tags:
        return "#Tech #TechDaily"
    hashtags = []
    for tag in tags[:6]:
        clean = tag.replace(" ", "").replace("-", "").replace("&", "").replace("/", "")
        hashtags.append(f"#{clean}")
    return " ".join(hashtags)

def send_message(chat_id, text, reply_markup=None):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }
    if reply_markup:
        payload["reply_markup"] = json.dumps(reply_markup)
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()

def build_inline_buttons(link):
    return {
        "inline_keyboard": [
            [{"text": "📖 Read Full Article", "url": link}],
            [{"text": "⚡ Join Our Private Channel", "url": "https://t.me/tribute/app?startapp=s12I"}]
        ]
    }

def main():
    title, link, description = get_latest_post()
    if not link:
        return

    last_url = load_last_post()
    if link == last_url:
        print("No new posts.")
        return

    print(f"New post detected: {title}")

    tags = get_post_tags(link)
    hashtags = format_tags(tags)

    post_message = (
        f"⚠️ <b>NEW BLOG ARTICLE ALERT</b> ‼️\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"📰 <b>{title}</b>\n\n"
        f"<blockquote>{description}</blockquote>\n\n"
        f"✦•━━━━━━•✦✦•━━━━━━•✦\n"
        f"💞 Keep Supporting Us 💞 ▬▬\n"
        f"🏷 Tags: {hashtags}"
    )

    buttons = build_inline_buttons(link)

    failed = []
    for channel in CHANNELS:
        try:
            send_message(channel, post_message, reply_markup=buttons)
            print(f"✅ Posted to {channel}")
        except Exception as e:
            failed.append(channel)
            print(f"❌ Failed to post to {channel}: {e}")

    # Admin notification
    status_lines = "\n".join(
        [f"{'✅' if ch not in failed else '❌'} {ch}" for ch in CHANNELS]
    )
    admin_message = (
        f"🔔 <b>New Post Published!</b>\n\n"
        f"📰 <b>{title}</b>\n"
        f"🔗 {link}\n\n"
        f"<b>Delivery Status:</b>\n"
        f"{status_lines}"
    )
    try:
        resp = send_message(ADMIN_CHAT, admin_message)
        print(f"✅ Admin notified at {ADMIN_CHAT}")
        print(f"   Telegram response: {resp}")
    except requests.exceptions.HTTPError as e:
        print(f"❌ Failed to notify admin: {e}")
        print(f"   Response body: {e.response.text}")

    save_last_post(link)
    print(f"Done: {title}")

if __name__ == "__main__":
    main()