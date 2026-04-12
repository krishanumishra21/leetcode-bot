# LeetCode Reminder Bot (Telegram + Cloud)

A smart automation system that tracks daily LeetCode activity and sends reminders via Telegram if no problem is solved.

---

##  Features

-  Tracks daily LeetCode submissions
-  Sends Telegram alerts if no problem is solved
-  Uses funny/savage messages for motivation
-  Runs automatically on scheduled times
-  Deployed on cloud (Render)
-  Secure environment variables support

---

##  Problem It Solves

Staying consistent with daily LeetCode practice is hard.  
This bot automates reminders so you never break your streak.

---

##  Tech Stack

- Python 
- LeetCode GraphQL API
- Telegram Bot API
- Flask (for deployment workaround)
- Render (cloud hosting)

---

##  Challenges & Solutions

### 1. Background Worker Required Paid Plan
-  Render background worker needed credits
-  Solution: Converted bot into Flask web service

### 2. Free Tier Sleep Issue
-  Render service sleeps after inactivity
-  Solution: Used UptimeRobot to ping every 5 minutes

### 3. Timezone Bug (UTC vs IST)
-  Server time mismatch caused missed triggers
-  Solution: Converted UTC → IST manually in code

---

## 📦 Setup (Local)

### 1. Clone Repo
```bash
git clone https://github.com/your-username/leetcode-bot.git
cd leetcode-bot
