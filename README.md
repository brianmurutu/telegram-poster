<div align="center">

```
██████╗ ██╗      ██████╗  ██████╗      ████████╗ ██████╗
██╔══██╗██║     ██╔═══██╗██╔════╝      ╚══██╔══╝██╔═══██╗
██████╔╝██║     ██║   ██║██║  ███╗        ██║   ██║   ██║
██╔══██╗██║     ██║   ██║██║   ██║        ██║   ██║   ██║
██████╔╝███████╗╚██████╔╝╚██████╔╝        ██║   ╚██████╔╝
╚═════╝ ╚══════╝ ╚═════╝  ╚═════╝         ╚═╝    ╚═════╝

████████╗███████╗██╗     ███████╗ ██████╗ ██████╗  █████╗ ███╗   ███╗
╚══██╔══╝██╔════╝██║     ██╔════╝██╔════╝ ██╔══██╗██╔══██╗████╗ ████║
   ██║   █████╗  ██║     █████╗  ██║  ███╗██████╔╝███████║██╔████╔██║
   ██║   ██╔══╝  ██║     ██╔══╝  ██║   ██║██╔══██╗██╔══██║██║╚██╔╝██║
   ██║   ███████╗███████╗███████╗╚██████╔╝██║  ██║██║  ██║██║ ╚═╝ ██║
   ╚═╝   ╚══════╝╚══════╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝
```

# 📡 Blog → Telegram Auto-Poster

### **v1.0** — Automatically detect new blog posts and instantly broadcast them to your Telegram channels with rich formatting, inline buttons, and personal admin notifications.

[![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-Automated-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)](https://github.com/features/actions)
[![Telegram Bot API](https://img.shields.io/badge/Telegram_Bot_API-v7-26A5E4?style=for-the-badge&logo=telegram&logoColor=white)](https://core.telegram.org/bots/api)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Version](https://img.shields.io/badge/Version-1.0-orange?style=for-the-badge)]()

</div>

---

## 📖 Table of Contents

- [What It Does](#-what-it-does)
- [How It Works](#-how-it-works)
- [Post Preview](#-post-preview)
- [Prerequisites](#-prerequisites)
- [Setup Guide](#-setup-guide)
  - [1. Create a Telegram Bot](#step-1-create-a-telegram-bot)
  - [2. Get Your Channel IDs](#step-2-get-your-channel-ids)
  - [3. Get Your Personal Chat ID](#step-3-get-your-personal-chat-id)
  - [4. Fork & Configure the Repo](#step-4-fork--configure-the-repo)
  - [5. Configure the Script](#step-5-configure-the-script)
  - [6. Add GitHub Secret](#step-6-add-github-secret)
  - [7. Deploy & Test](#step-7-deploy--test)
- [Configuration Reference](#-configuration-reference)
- [Customizing Your Post Format](#-customizing-your-post-format)
- [Troubleshooting](#-troubleshooting)
- [FAQ](#-faq)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ What It Does

This bot monitors your blog's homepage every **15 minutes** using a scheduled GitHub Actions workflow. The moment a new article is detected, it:

- 📢 **Broadcasts** a beautifully formatted post to **multiple Telegram channels** simultaneously
- 📰 **Extracts** the article title, meta description, and tags automatically from your blog
- 🏷️ **Converts** your blog's tags into Telegram hashtags dynamically
- 🔘 **Attaches** inline action buttons (Read Article + Join Channel CTA)
- 🔔 **Notifies** you personally in your Telegram DMs with a delivery status report
- 💾 **Remembers** the last posted article to avoid duplicate posts
- ✅ **Fault-tolerant** — if one channel fails, others still receive the post

**Zero server required. Runs entirely free on GitHub Actions.**

---

## ⚙️ How It Works

```
┌─────────────────────────────────────────────────────────────┐
│                  GitHub Actions (every 15 min)               │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
              ┌────────────────────────┐
              │  Fetch Blog Homepage   │
              │  (BeautifulSoup scrape)│
              └───────────┬────────────┘
                          │
              ┌───────────▼────────────┐
              │  Compare with          │
              │  last_post.json        │
              └───────────┬────────────┘
                          │
               ┌──────────▼──────────┐
               │   New post found?   │
               └──────────┬──────────┘
                    YES    │     NO
          ┌───────────────┘     └──────────────────┐
          ▼                                         ▼
┌─────────────────────┐                   ┌──────────────────┐
│  Scrape post page   │                   │  Exit. No action.│
│  - Title            │                   └──────────────────┘
│  - Meta description │
│  - Tags/hashtags    │
└────────┬────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│         Send to Telegram channels        │
│  ┌──────────────┐  ┌──────────────────┐ │
│  │ @channel_one │  │  @channel_two    │ │
│  └──────────────┘  └──────────────────┘ │
└────────────────────┬────────────────────┘
                     │
                     ▼
          ┌──────────────────────┐
          │  Notify admin DM     │
          │  with delivery report│
          └──────────────────────┘
                     │
                     ▼
          ┌──────────────────────┐
          │  Save new post URL   │
          │  to last_post.json   │
          │  Commit & push       │
          └──────────────────────┘
```

---

## 📱 Post Preview

Here is what every post looks like when it lands in your Telegram channel:

```
⚠️ NEW BLOG ARTICLE ALERT ‼️
━━━━━━━━━━━━━━━━━━━━

📰 What Is an AI Agent? How to Automate Your Work in 2026

▎ A deep dive into the transition from "talking to AI"
▎ to "AI doing the work." This guide explains what AI
▎ agents are, why they matter for productivity...

✦•━━━━━━•✦✦•━━━━━━•✦
💞 Keep Supporting Us 💞 ▬▬
🏷 Tags: #Tech #TechDaily #AIAgents #Cybersecurity

┌─────────────────────────────┐
│     📖 Read Full Article     │
├─────────────────────────────┤
│  ⚡ Join Our Private Channel │
└─────────────────────────────┘
```

And your personal admin notification looks like:

```
🔔 New Post Published!

📰 What Is an AI Agent?...
🔗 https://yourblog.com/article-slug

Delivery Status:
✅ @channel_one
✅ @channel_two
```

---

## 🧰 Prerequisites

Before you begin, make sure you have:

- ✅ A **blog or website** (any CMS — WordPress, Ghost, custom, etc.)
- ✅ A **GitHub account** (free)
- ✅ A **Telegram account**
- ✅ One or more **Telegram channels** where you are the owner/admin
- ✅ Basic comfort with editing a text file

No coding experience required beyond editing a few config lines.

---

## 🚀 Setup Guide

### Step 1: Create a Telegram Bot

1. Open Telegram and search for **@BotFather**
2. Send the command `/newbot`
3. Follow the prompts — choose a name and a username for your bot (username must end in `bot`, e.g. `myblogposter_bot`)
4. BotFather will reply with your **Bot Token** — it looks like:
   ```
   7123456789:AAGcXXXXXXXXXXXXXXXXXXXXXXXXXXX
   ```
5. **Copy and save this token** — you will need it in Step 6

> ⚠️ **Never share your bot token publicly.** Anyone with it can control your bot.

---

### Step 2: Add Your Bot as Channel Admin

For **each Telegram channel** you want to post to:

1. Open your channel in Telegram
2. Go to **Channel Info → Administrators → Add Administrator**
3. Search for your bot's username and add it
4. Grant it **Post Messages** permission (minimum required)
5. Save

---

### Step 3: Get Your Personal Chat ID

The bot needs your **numeric user ID** (not your username) to send you personal notifications.

1. Open Telegram and search for **@userinfobot**
2. Send it `/start`
3. It will reply with something like:
   ```
   Id: 123456789
   First: John
   ```
4. **Copy the numeric ID** — you will use it in the script

> 💡 Also send `/start` to **your own bot** in a private DM — this is required before it can message you.

---

### Step 4: Fork & Configure the Repo

1. Click **Fork** at the top right of this repository
2. Clone your fork locally or edit files directly on GitHub:
   ```bash
   git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   cd YOUR_REPO_NAME
   ```

---

### Step 5: Configure the Script

Open `notify.py` and update the following lines at the top of the file:

```python
# ─── YOUR CONFIGURATION ───────────────────────────────────────

# Your Telegram channel usernames (add as many as you need)
CHANNELS = ["@your_channel_one", "@your_channel_two"]

# Your personal Telegram numeric user ID (from @userinfobot)
ADMIN_CHAT = "123456789"

# Your blog's homepage URL
BLOG_URL = "https://yourblog.com"

# ──────────────────────────────────────────────────────────────
```

Then update the **inline buttons** to match your links. Find the `build_inline_buttons` function:

```python
def build_inline_buttons(link):
    return {
        "inline_keyboard": [
            [
                {"text": "📖 Read Full Article", "url": link}
            ],
            [
                # Replace this URL with your own CTA link
                {"text": "⚡ Join Our Private Channel", "url": "https://t.me/YOUR_INVITE_LINK"}
            ]
        ]
    }
```

Also update the homepage scraper if your blog uses a different HTML structure. By default the script targets `<h2>` tags containing article links. If your blog uses `<h3>` or `<article>` tags, update this function:

```python
def get_latest_post():
    # ...
    for tag in soup.find_all("h2"):   # ← change "h2" to match your blog's HTML
        a = tag.find("a", href=True)
        if a and a["href"].startswith("https://yourblog.com/"):
```

> 💡 **Tip:** Open your blog in Chrome → right-click an article title → **Inspect** to see what HTML tag wraps the title links.

---

### Step 6: Add GitHub Secret

Your bot token must be stored securely as a GitHub secret — never hardcoded in the script.

1. Go to your forked repository on GitHub
2. Click **Settings → Secrets and variables → Actions**
3. Click **New repository secret**
4. Set:
   - **Name:** `TELEGRAM_BOT_TOKEN`
   - **Value:** your bot token from Step 1
5. Click **Add secret**

---

### Step 7: Deploy & Test

**Commit your changes:**
```bash
git add notify.py
git commit -m "feat: configure bot for my blog and channels"
git push
```

**Run a manual test:**
1. Go to your repo on GitHub → **Actions** tab
2. Click **Blog to Telegram Notifier**
3. Click **Run workflow → Run workflow**
4. Watch the logs — you should see:
   ```
   ✅ Posted to @your_channel_one
   ✅ Posted to @your_channel_two
   ✅ Admin notified at 123456789
   Done: Your Latest Post Title
   ```
5. Check your Telegram channels and DMs 🎉

From this point on the workflow runs **automatically every 15 minutes** on its own.

---

## 🔧 Configuration Reference

| Variable | Location | Description |
|---|---|---|
| `TELEGRAM_BOT_TOKEN` | GitHub Secret | Your bot token from @BotFather |
| `CHANNELS` | `notify.py` line 9 | List of channel usernames to post to |
| `ADMIN_CHAT` | `notify.py` line 10 | Your numeric Telegram user ID |
| `BLOG_URL` | `notify.py` line 12 | Your blog's homepage URL |
| `STATE_FILE` | `notify.py` line 13 | Filename to track last posted article |
| Cron schedule | `telegram-notify.yml` line 5 | How often to check for new posts |

**Changing the check frequency:**

Edit the cron expression in `.github/workflows/telegram-notify.yml`:

```yaml
schedule:
  - cron: '*/15 * * * *'   # Every 15 minutes (default)
  - cron: '*/5 * * * *'    # Every 5 minutes
  - cron: '0 * * * *'      # Every hour
  - cron: '0 9 * * *'      # Once daily at 9am UTC
```

> ⚠️ GitHub Actions free tier has limits. Checking every 5 minutes on an active repo is fine; every 1 minute may hit rate limits.

---

## 🎨 Customizing Your Post Format

The post message is built in the `main()` function inside `notify.py`. Edit this block to change the layout:

```python
post_message = (
    f"⚠️ <b>NEW BLOG ARTICLE ALERT</b> ‼️\n"
    f"━━━━━━━━━━━━━━━━━━━━\n\n"
    f"📰 <b>{title}</b>\n\n"
    f"<blockquote>{description}</blockquote>\n\n"
    f"✦•━━━━━━•✦✦•━━━━━━•✦\n"
    f"💞 Keep Supporting Us 💞 ▬▬\n"
    f"🏷 Tags: {hashtags}"
)
```

**Telegram HTML formatting tags you can use:**

| Tag | Effect | Example |
|---|---|---|
| `<b>text</b>` | **Bold** | `<b>Breaking</b>` |
| `<i>text</i>` | _Italic_ | `<i>subtitle</i>` |
| `<u>text</u>` | Underline | `<u>important</u>` |
| `<blockquote>text</blockquote>` | Quote block | Description excerpts |
| `<a href="url">text</a>` | Hyperlink | `<a href="...">Read</a>` |
| `<code>text</code>` | Monospace | Code snippets |

---

## 🛠 Troubleshooting

**❌ Exit code 1 — KeyError: TELEGRAM_BOT_TOKEN**
Your GitHub secret is missing or misspelled. Go to **Settings → Secrets → Actions** and confirm the secret is named exactly `TELEGRAM_BOT_TOKEN`.

**❌ 403 Forbidden when posting to channel**
Your bot has not been added as an administrator to the channel. See [Step 2](#step-2-add-your-bot-as-channel-admin).

**❌ Bot cannot message me personally (admin notification fails)**
Two possible causes:
- You haven't sent `/start` to your bot in a private DM yet
- You used `@username` instead of the numeric user ID. Get your ID from [@userinfobot](https://t.me/userinfobot)

**❌ No posts found / script says "Could not find any posts"**
Your blog's HTML structure differs from the default. Open your blog → right-click an article title → Inspect Element → identify the tag wrapping the title link and update the `get_latest_post()` function accordingly.

**❌ Exit code 128 — git push fails**
The workflow couldn't commit `last_post.json` back to the repo. Make sure the `GITHUB_TOKEN` has write permissions: go to **Settings → Actions → General → Workflow permissions** → select **Read and write permissions**.

**⚠️ Posts duplicate on the same channel**
You have the same channel listed twice — once as a numeric ID and once as a username. They refer to the same channel. Keep only the username format: `@channel_name`.

---

## ❓ FAQ

**Does this work with WordPress?**
Yes. WordPress blogs expose article links in `<h2>` tags by default on most themes. If your theme is different, inspect your homepage HTML and update the `get_latest_post()` function to match.

**Does this work with Ghost, Webflow, or custom CMS?**
Yes, as long as the blog homepage lists articles as HTML links. Alternatively, if your platform provides an RSS feed, you can switch back to `feedparser` for a more reliable detection method.

**Can I post to more than two channels?**
Yes. Just add more usernames to the `CHANNELS` list:
```python
CHANNELS = ["@channel_one", "@channel_two", "@channel_three", "@channel_four"]
```

**Will it re-post old articles?**
No. Once an article URL is saved to `last_post.json`, it will never be posted again unless you manually delete that file from the repository.

**Can I add an image/thumbnail to the post?**
Yes — this requires using Telegram's `sendPhoto` API method instead of `sendMessage`. This is planned for a future version.

**Is this free to run?**
Yes. GitHub Actions provides 2,000 free minutes per month on free accounts. A workflow running every 15 minutes uses roughly 1–2 minutes per run × ~2,880 runs/month = well within free tier limits.

**What if GitHub Actions is down?**
Posts will be delayed until the next successful workflow run. The bot will catch up and post when Actions resumes, as long as the homepage still shows the new article.

---

## 🤝 Contributing

Contributions are welcome! If you have ideas for improvements — RSS feed support, image attachments, multiple blog sources, formatting options — feel free to open an issue or submit a pull request.

1. Fork the repo
2. Create a feature branch: `git checkout -b feat/your-feature-name`
3. Commit your changes: `git commit -m "feat: describe your change"`
4. Push and open a Pull Request

Please keep PRs focused and well-described.

---

## 📄 License

This project is licensed under the **MIT License** — you are free to use, modify, and distribute it for personal or commercial purposes. See [LICENSE](LICENSE) for full details.

---

<div align="center">

Built with ❤️ by **[Sir. brian](https://sir-brian.top)**

📢 [Join our Telegram Channel](https://t.me/techdaily_buzz) · 🌐 [Visit the Blog](https://techdaily.buzz)

</div>
