import os
import requests
import json
import time
import random
import threading
from datetime import datetime, timedelta
from dotenv import load_dotenv
from flask import Flask

load_dotenv()

# 🌐 Flask app
app = Flask(__name__)

@app.route("/")
def home():
    return "🚀 LeetCode Bot Running!"

# 🔐 CONFIG
USERNAMES = ["krishanu2109"]

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# ⏰ TIMES (ADDED 10:48 + 10:57)
TIMES = [
    "10:48",
    "11:01","11:10","11:30",
    "20:00", "20:15", "20:30", "20:45",
    "21:00", "21:15", "21:30",
    "22:00", "22:15", "22:30", "22:45",
    "23:00", "23:15", "23:30", "23:45",
    "01:29", "01:36", "01:53"
]

# 😂 FUNNY MESSAGES
def get_funny_message(user, solved):
    if solved:
        msgs = [
            f"🔥 WAH {user}!! Aaj bhi solve kar diya 💪\nStreak strong hai ⚡",
            f"😎 {user} OP hai bhai!\nDaily coding chal rahi hai 🚀",
            f"💯 {user} ne phir se LeetCode pe maar diya!\nConsistency level MAX 🔥"
        ]
    else:
        msgs = [
            f"🚨 Oye {user}!! Solve kar le bhai 😤\nwarna streak gaya... GAYA 💀",
            f"😡 {user} kya kar raha hai?\nLeetCode wait kar raha hai aur tu chill kar raha hai? 🤡",
            f"⚠️ {user} ALERT!!\nStreak danger mein hai 🚨\nAbhi solve kar warna RIP 💀",
            f"😂 {user} bhai serious ho ja\nStreak bolega: 'main chala' 🚶‍♂️💀",
            f"😴 {user} uth ja bhai!\nLeetCode ro raha hai 😭\nCode maar 💻🔥"
        ]
    return random.choice(msgs)

# 📲 TELEGRAM
def send_telegram(msg):
    print("📤 Sending:", msg)

    if not BOT_TOKEN or not CHAT_ID:
        print("❌ BOT_TOKEN or CHAT_ID missing")
        return

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    try:
        res = requests.post(url, data={"chat_id": CHAT_ID, "text": msg})
        print("📩 Response:", res.text)
    except Exception as e:
        print("❌ Telegram error:", e)

# 🔍 CHECK LEETCODE
def check_leetcode(username):
    try:
        url = "https://leetcode.com/graphql"

        query = {
            "query": """
            query getUserProfile($username: String!) {
              matchedUser(username: $username) {
                submissionCalendar
              }
            }
            """,
            "variables": {"username": username}
        }

        res = requests.post(url, json=query)
        data = res.json()

        calendar = json.loads(data['data']['matchedUser']['submissionCalendar'])

        # ✅ IST date
        today = (datetime.utcnow() + timedelta(hours=5, minutes=30)).date()

        for ts in calendar:
            date = datetime.fromtimestamp(int(ts)).date()
            if date == today:
                return True

        return False

    except Exception as e:
        print(f"❌ Error for {username}:", e)
        return False


# 🔁 BOT LOOP
def run_bot():
    already_sent = set()
    current_day = (datetime.utcnow() + timedelta(hours=5, minutes=30)).date()

    print("🔥 BOT LOOP STARTED")
    send_telegram("🚀 BOT STARTED SUCCESSFULLY")

    while True:
        try:
            # ✅ CONVERT UTC → IST
            now = datetime.utcnow() + timedelta(hours=5, minutes=30)
            now_time = now.strftime("%H:%M")
            today = now.date()

            print("⏰ IST TIME:", now_time)  # DEBUG

            # 🔄 Reset daily
            if today != current_day:
                already_sent.clear()
                current_day = today
                print("🔄 New day reset")

            # ✅ EXACT MATCH LOGIC
            for t in TIMES:
                if now_time == t and t not in already_sent:
                    print(f"⏰ Running at {t}")

                    message = "📊 LeetCode Daily Report:\n\n"

                    for user in USERNAMES:
                        solved = check_leetcode(user)
                        message += get_funny_message(user, solved) + "\n\n"

                    send_telegram(message)
                    already_sent.add(t)

            time.sleep(10)

        except Exception as e:
            print("❌ Loop error:", e)
            time.sleep(10)


# 🚀 START
if __name__ == "__main__":
    print("🚀 Starting bot thread...")

    bot_thread = threading.Thread(target=run_bot)
    bot_thread.daemon = True
    bot_thread.start()

    app.run(host="0.0.0.0", port=10000)
