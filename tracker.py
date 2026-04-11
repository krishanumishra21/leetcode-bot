import os
import requests
import json
import time
import random
import threading
from datetime import datetime
from dotenv import load_dotenv
from flask import Flask

load_dotenv()

# 🌐 Flask app (for Render free web service)
app = Flask(__name__)

@app.route("/")
def home():
    return "🚀 LeetCode Bot Running!"

# 🔐 CONFIG
USERNAMES = ["krishanu2109"]

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

TIMES = [
    "20:00", "20:15", "20:30", "20:45",
    "21:00", "21:15", "21:30","10:11",
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
    if not BOT_TOKEN or not CHAT_ID:
        print("❌ BOT_TOKEN or CHAT_ID missing")
        return

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, data={"chat_id": CHAT_ID, "text": msg})
        print("📩 Message sent")
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
        today = datetime.now().date()

        for ts in calendar:
            date = datetime.fromtimestamp(int(ts)).date()
            if date == today:
                return True

        return False

    except Exception as e:
        print(f"❌ Error for {username}:", e)
        return False


# 🔁 BOT LOOP (thread)
def run_bot():
    already_sent = set()
    current_day = datetime.now().date()

    print("🚀 Savage bot started... 😎")

    while True:
        try:
            now = datetime.now()
            now_time = now.strftime("%H:%M")
            today = now.date()

            # 🔄 Reset daily
            if today != current_day:
                already_sent.clear()
                current_day = today
                print("🔄 New day reset")

            # ⏰ CHECK TIMES
            for t in TIMES:
                if now_time == t and t not in already_sent:
                    print(f"⏰ Running at {t}")

                    message = "📊 LeetCode Daily Report:\n\n"

                    for user in USERNAMES:
                        solved = check_leetcode(user)
                        message += get_funny_message(user, solved) + "\n\n"

                    send_telegram(message)
                    already_sent.add(t)

            time.sleep(30)

        except Exception as e:
            print("❌ Loop error:", e)
            time.sleep(30)


# 🚀 START BOTH
if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    app.run(host="0.0.0.0", port=10000)
