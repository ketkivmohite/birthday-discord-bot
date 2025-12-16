# 🎂 Birthday Discord Bot

A fun, friendly Discord bot that remembers birthdays and sends personalized birthday messages throughout the day — so no one ever feels forgotten again 💖

Built with **Python**, **discord.py**, and deployed on **Railway**.

---

## ✨ Features

* 👋 Greets users when they say **hi**
* 🧠 Asks and stores:

  * Name
  * Birthday (YYYY-MM-DD)
* 🎉 Automatically wishes users on their birthday
* 💌 Sends warm, goofy, close-friend style birthday messages
* ☁️ Fully deployed & running 24/7 on Railway
* 🔒 Uses environment variables for security

---

## 🛠 Tech Stack

* **Python 3**
* **discord.py**
* **Railway** (deployment)
* **GitHub** (version control)

---

## 📁 Project Structure

```
birthday-discord-bot/
│
├── bot.py              # Main bot logic
├── requirements.txt    # Python dependencies
├── Procfile            # Railway worker config
├── .gitignore
└── README.md
```

---

## 🚀 How It Works

1. User types **hi** in a Discord channel
2. Bot asks for the user’s name
3. Bot asks for their birthday (YYYY-MM-DD)
4. Bot saves the data
5. On the user’s birthday 🎂:

   * Bot automatically sends a birthday message
   * No need for manual reminders

---

## 🔐 Environment Variables

The bot requires the following environment variable:

```
DISCORD_BOT_TOKEN=your_discord_bot_token_here
```

This is configured securely in **Railway → Variables**
❌ Never hardcode your token.

---

## 📦 Installation (Local Setup)

```bash
git clone https://github.com/ketkivmohite/birthday-discord-bot.git
cd birthday-discord-bot
pip install -r requirements.txt
python bot.py
```

Make sure you set `DISCORD_BOT_TOKEN` before running.

---

## ☁️ Deployment (Railway)

* Connect the GitHub repo to Railway
* Add `DISCORD_BOT_TOKEN` in Variables
* Procfile:

  ```
  worker: python bot.py
  ```
* Deploy 🎉

Once deployed, the bot stays online automatically.

---

## 🧪 Testing

* Say **hi** in the Discord server
* Enter your name and birthday
* Wait for your birthday 🎂
* Enjoy the message ✨

---

## 💡 Future Improvements

* Multiple birthday messages throughout the day
* Timezone support
* Admin commands
* Database support (instead of in-memory storage)
* Slash commands (`/birthday`, `/setbirthday`)

---

## ❤️ Author

Built with love by **Ketki Mohite**
A learning project turned real, deployed, and working 🚀


