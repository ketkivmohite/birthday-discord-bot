import discord
from discord.ext import commands, tasks
from datetime import datetime
import json
import random
import os

# ---------------- BOT SETUP ----------------
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

USERS_FILE = "users.json"

# 🔐 ADMIN (ONLY YOU)
ADMIN_IDS = ["794881710709538816"]  # ✅ your Discord user ID

# ---------------- MESSAGE POOL ----------------
EVERGREEN_MESSAGES = [
    "Happy birthday. Still wild that someone this cool exists.",
    "Another year of you being effortlessly iconic.",
    "Main character energy looks good on you.",
    "Don’t let the attention get to your head — impossible, I know.",
    "You age like someone who knows their worth.",
    "I’d roast you, but today you’re protected.",
    "Same you, new year — elite combo.",
    "You make life better just by being here.",
    "You’re chaos, but the lovable kind.",
    "That birthday glow is LOUD.",
    "Thanks for existing. Genuinely.",
    "You’re someone people are lucky to have.",
    "Another year of being unforgettable.",
    "You make growing up look survivable.",
    "You matter. Even when you forget it.",
    "You don’t force it — that’s why it works.",
    "Life upgraded when you showed up.",
    "You’re still you. Huge compliment.",
    "Today suits you perfectly."
]

# ---------------- TEMP REGISTRATION STATE ----------------
registration_state = {}

# ---------------- FILE HELPERS ----------------
def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(data):
    with open(USERS_FILE, "w") as f:
        json.dump(data, f, indent=4)

# ---------------- READY ----------------
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    birthday_checker.start()

# ---------------- MESSAGE BUILDERS ----------------
def midnight_message(name, age):
    return (
        f"🎂 Happy Birthday, {name}.\n\n"
        f"You turn {age} today.\n"
        f"A brand new year starts now."
    )

def final_blessing(name):
    return (
        f"🌙 As this birthday ends, {name}…\n\n"
        f"You showed up.\n"
        f"And that mattered."
    )

# ---------------- TEST BIRTHDAY MODE (ADMIN ONLY) ----------------
async def run_test_birthday(user_id, data):
    user = await bot.fetch_user(int(user_id))
    name = data["name"]

    year = datetime.now().year
    age = year - int(data["birthday"][:4])

    messages = random.sample(
        EVERGREEN_MESSAGES,
        min(age, len(EVERGREEN_MESSAGES))
    )

    await user.send(midnight_message(name, age))

    for msg in messages:
        await user.send(msg)

    await user.send(final_blessing(name))

# ---------------- CONVERSATIONAL FLOW ----------------
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    user_id = str(message.author.id)
    users = load_users()
    content = message.content.strip().lower()

    # ---- HELP ----
    if content == "help":
        await message.channel.send(
            "👋 **BirthdayBot Help** 🎂\n\n"
            "• Say **hi** to register your birthday\n"
            "• I’ll DM you messages on your birthday 💖\n"
            "• I’m soft, subtle, and always rooting for you 🌷\n"
            "• That’s it — simple and sweet ✨"
        )
        return

    # ---- TEST MODE (YOU ONLY) ----
    if content == "testbirthday":
        if user_id not in ADMIN_IDS:
            await message.channel.send("🚫 Test mode is only for the bot owner.")
            return

        if user_id not in users:
            await message.channel.send("You’re not registered yet 😅\nSay **hi** first.")
            return

        await message.channel.send("🧪 Test mode ON!\nCheck your DMs 🎂")
        await run_test_birthday(user_id, users[user_id])
        return

    # ---- GREETING ----
    if content in ["hi", "hello", "hey", "hii"]:
        if user_id in users:
            await message.channel.send(
                f"Hey {users[user_id]['name']} 🌸\nI’ve got your birthday saved 🎂"
            )
        else:
            registration_state[user_id] = {"step": "name"}
            await message.channel.send("Hey 🌸\nWhat’s your name?")
        return

    # ---- REGISTRATION FLOW ----
    if user_id in registration_state:
        step = registration_state[user_id]["step"]

        if step == "name":
            registration_state[user_id]["name"] = message.content.strip()
            registration_state[user_id]["step"] = "birthday"
            await message.channel.send(
                f"Nice to meet you, {message.content.strip()} 💫\n"
                f"When’s your birthday? (YYYY-MM-DD)"
            )
            return

        if step == "birthday":
            try:
                datetime.strptime(message.content.strip(), "%Y-%m-%d")
            except ValueError:
                await message.channel.send(
                    "That format’s a little chaotic 😭\nTry: **YYYY-MM-DD**"
                )
                return

            users[user_id] = {
                "name": registration_state[user_id]["name"],
                "birthday": message.content.strip(),
                "messages": [],
                "sent_today": 0,
                "midnight_sent": False,
                "final_sent": False,
                "last_birthday_year": None
            }

            save_users(users)
            del registration_state[user_id]

            await message.channel.send(
                f"🎁 All set, {users[user_id]['name']}!\n"
                f"I’ll remember your birthday and hype you properly 💖"
            )
            return

# ---------------- BIRTHDAY CHECKER ----------------
@tasks.loop(minutes=1)
async def birthday_checker():
    now = datetime.now()
    today = now.strftime("%m-%d")
    year = now.year
    minute_now = now.hour * 60 + now.minute

    users = load_users()
    updated = False

    for uid, data in users.items():

        if data.get("last_birthday_year") == year:
            continue

        if data["birthday"][5:] != today:
            data["sent_today"] = 0
            data["midnight_sent"] = False
            data["final_sent"] = False
            data["messages"] = []
            continue

        user = await bot.fetch_user(int(uid))
        name = data["name"]
        age = year - int(data["birthday"][:4])

        if not data["messages"]:
            data["messages"] = random.sample(
                EVERGREEN_MESSAGES,
                min(age, len(EVERGREEN_MESSAGES))
            )

        if minute_now == 0 and not data["midnight_sent"]:
            await user.send(midnight_message(name, age))
            data["midnight_sent"] = True
            updated = True

        if data["sent_today"] < age:
            interval = max(1, 1440 // age)
            if minute_now == data["sent_today"] * interval:
                await user.send(data["messages"][data["sent_today"]])
                data["sent_today"] += 1
                updated = True

        if minute_now == 1439 and not data["final_sent"]:
            await user.send(final_blessing(name))
            data["final_sent"] = True
            data["last_birthday_year"] = year
            updated = True

    if updated:
        save_users(users)

# ---------------- RUN ----------------
bot.run(os.getenv("DISCORD_BOT_TOKEN"))
