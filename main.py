import discord
import random
import json
import os

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

# Load or create data file
if os.path.exists("data.json"):
    with open("data.json", "r") as f:
        data = json.load(f)
else:
    data = {}

def save_data():
    with open("data.json", "w") as f:
        json.dump(data, f)

def get_level(xp):
    return int(xp ** 0.5)

@client.event
async def on_ready():
    print(f"Bot is online as {client.user}")

@client.event
async def on_message(message):
    if message.author.bot:
        return

    user_id = str(message.author.id)

    if user_id not in data:
        data[user_id] = {"xp": 0, "level": 0}

    xp_gain = random.randint(5, 15)
    data[user_id]["xp"] += xp_gain

    xp = data[user_id]["xp"]
    level = data[user_id]["level"]
    new_level = get_level(xp)

    if new_level > level:
        data[user_id]["level"] = new_level
        await message.channel.send(
            f"{message.author.mention} reached Level {new_level}! 🎉"
        )

    save_data()

    # Rank
    if message.content == "!rank":
        await message.channel.send(
            f"{message.author.mention} | Level: {data[user_id]['level']} | XP: {data[user_id]['xp']}"
        )

    # Leaderboard
    if message.content == "!leaderboard":
        sorted_users = sorted(data.items(), key=lambda x: x[1]["xp"], reverse=True)

        text = "**🏆 TOP PLAYERS 🏆**\n\n"

        for i, (uid, info) in enumerate(sorted_users[:5], start=1):
            try:
                user = await client.fetch_user(int(uid))
                text += f"{i}. {user.name} — {info['xp']} XP\n"
            except:
                continue

        await message.channel.send(text)

# IMPORTANT (token from environment)
client.run(os.getenv("MTQ5MzQ4Mjg4NzkzNTQyNjY1MA.G9MptM.5sBMkagzM861KN6hzlNaanbCojfZwJXK2bsKLc"))
