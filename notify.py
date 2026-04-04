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

def get_post_details(post_url):
    """Fetch the individual post page to get description and tags."""
    response = requests.get(post_url, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    # --- Description ---
    description = ""
    meta_desc = soup.find("meta", attrs={"name": "description"})
    if meta_desc and meta_desc.get("content"):
        description = meta_desc["content"].strip()

    # Fallback: first paragraph after the h1
    if not description:
        h1 = soup.find("h1")
        if h1:
            next_p = h1.find_next("p")
            if next_p:
                description = next_p.get_text(strip=True)

    # Trim to 200 chars
    if len(description) > 200:
        description = description[:200].rsplit(" ", 1)[0] + "..."

    # --- Tags ---
    tags = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if "/tag/" in href:
            tag_text = a.get_text(strip=True)
            if tag_text and tag_text not in tags:
                tags.append(tag_text)

    return description, tags

def format_tags(tags):
    """Convert tag list to hashtag string."""
    if not tags:
        return "#Tech #TechDaily"
    hashtags = []
    for tag in tags[:6]:  # limit to 6 tags
        clean = tag.replace(" ", "").replace("-", "").replace("&", "").replace("/", "")
        hashtags.append(f"#{clean}")
    return " ".join(hashtags)

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

    description, tags = get_post_details(link)
    hashtags = format_tags(tags)

    message = (
        f"📰 <b>{title}</b>\n\n"
        f"{description}\n\n"
        f"🔗 <a href='{link}'>Read Full Article</a>\n\n"
        f"✦•━━━━━━•✦✦•━━━━━━•✦\n"
        f"💞 Keep Supporting Us 💞 ▬▬\n"
        f"🏷 Tags: {hashtags}"
    )

    send_telegram_message(message)
    save_last_post(link)
    print(f"Posted: {title}")

if __name__ == "__main__":
    main()