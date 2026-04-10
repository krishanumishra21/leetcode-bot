import os
import requests
import json
import time
from datetime import datetime
from dotenv import load_dotenv


load_dotenv()


USERNAMES = [ "krishanu2109"]

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


TIMES = [
    "20:00", "20:15", "20:30", "20:45",
    "21:00", "21:15", "21:30", "22:45",
    "22:00", "22:15", "22:30", "21:54",
    "23:00", "23:15", "23:30", "23:45",
    "1:11"
]


def send_telegram(msg):
    if not BOT_TOKEN or not CHAT_ID:
        print("❌ BOT_TOKEN or CHAT_ID missing")
        return

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, data={"chat_id": CHAT_ID, "text": msg})
    except Exception as e:
        print("❌ Telegram error:", e)



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
        print(f" Error for {username}:", e)
        return False



already_sent = set()
current_day = datetime.now().date()

print("🚀 Multi-user bot started...")

while True:
    try:
        now_time = datetime.now().strftime("%H:%M")
        today = datetime.now().date()

       
        if today != current_day:
            already_sent.clear()
            current_day = today
            print(" New day reset")

      
        if now_time in TIMES and now_time not in already_sent:
            print(f" Running at {now_time}")

            message = " LeetCode Daily Report:\n\n"

            for user in USERNAMES:
                solved = check_leetcode(user)

                if solved:
                    message += f" {user} solved today \n"
                else:
                    message += f" {user} NOT solved \n"

            send_telegram(message)
            already_sent.add(now_time)

        time.sleep(30)

    except Exception as e:
        print(" Loop error:", e)
        time.sleep(30)
