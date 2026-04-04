import os
import json
import requests
from bs4 import BeautifulSoup

TELEGRAM_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHANNEL_ID = "-1002076804696"
BLOG_URL = "https://techdaily.buzz"
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
    response = requests.get(BLOG_URL, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    # Grab the first article h2 link on the homepage
    for tag in soup.find_all("h2"):
        a = tag.find("a", href=True)
        if a and a["href"].startswith("https://techdaily.buzz/"):
            title = a.get_text(strip=True)
            link = a["href"]
            return title, link
    return None, None

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
    title, link = get_latest_post()
    if not title:
        print("Could not find any posts on the homepage.")
        return

    last_url = load_last_post()

    if link == last_url:
        print("No new posts.")
        return

    message = f"📰 <b>{title}</b>\n\n🔗 <a href='{link}'>Read more on TechDaily</a>"
    send_telegram_message(message)
    save_last_post(link)
    print(f"Posted: {title}")

if __name__ == "__main__":
    main()