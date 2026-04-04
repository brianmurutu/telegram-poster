import os
import json
import requests
from bs4 import BeautifulSoup

TELEGRAM_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]

# All targets: channels + your personal inbox
CHANNELS = ["@techdaily_buzz", "@tech_empire"]
ADMIN_CHAT = "5134479845"  # Get this from @userinfobot on Telegram

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

    for tag in soup.find_all("h2"):
        a = tag.find("a", href=True)
        if a and a["href"].startswith("https://techdaily.buzz/"):
            title = a.get_text(strip=True)
            link = a["href"]
            return title, link
    return None, None

def get_post_details(post_url):
    response = requests.get(post_url, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    # Description
    description = ""
    meta_desc = soup.find("meta", attrs={"name": "description"})
    if meta_desc and meta_desc.get("content"):
        description = meta_desc["content"].strip()

    if not description:
        h1 = soup.find("h1")
        if h1:
            next_p = h1.find_next("p")
            if next_p:
                description = next_p.get_text(strip=True)

    if len(description) > 200:
        description = description[:200].rsplit(" ", 1)[0] + "..."

    # Tags
    tags = []
    for a in soup.find_all("a", href=True):
        if "/tag/" in a["href"]:
            tag_text = a.get_text(strip=True)
            if tag_text and tag_text not in tags:
                tags.append(tag_text)

    return description, tags

def format_tags(tags):
    if not tags:
        return "#Tech #TechDaily"
    hashtags = []
    for tag in tags[:6]:
        clean = tag.replace(" ", "").replace("-", "").replace("&", "").replace("/", "")
        hashtags.append(f"#{clean}")
    return " ".join(hashtags)

def send_message(chat_id, text, reply_markup=None):
    """Send a message to any chat ID or username."""
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
    """Build inline keyboard buttons for the post."""
    return {
        "inline_keyboard": [
            [
                {"text": "📖 Read Full Article", "url": link}
            ],
            [
                {"text": "⚡ Join Our Private Channel", "url": "https://t.me/tribute/app?startapp=s12I"}
            ]
        ]
    }

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

    # Main post message (sent to channels)
    post_message = (
        f"📰 <b>{title}</b>\n\n"
        f"<blockquote>{description}</blockquote>\n\n"
        f"✦•━━━━━━•✦✦•━━━━━━•✦\n"
        f"💞 Keep Supporting Us 💞 ▬▬\n"
        f"🏷 Tags: {hashtags}"
    )

    buttons = build_inline_buttons(link)

    # Post to all channels with buttons
    failed = []
    for channel in CHANNELS:
        try:
            send_message(channel, post_message, reply_markup=buttons)
            print(f"✅ Posted to {channel}")
        except Exception as e:
            failed.append(channel)
            print(f"❌ Failed to post to {channel}: {e}")

    # Send admin notification to personal inbox
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