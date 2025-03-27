import discord
from discord.ext import commands
import asyncio
import json
import configparser
from watch import watch_users

config = configparser.ConfigParser()
config.read("config.ini")

TOKEN = config["discord"]["token"]
FORUM_CHANNEL_ID = int(config["discord"]["forum_channel_id"])
TAG_ID = int(config["discord"]["tag_id"])

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

bot = commands.Bot(command_prefix="!", intents=intents)

usernames_file = "usernames.json"

def load_usernames():
    try:
        with open(usernames_file, "r") as f:
            return json.load(f)
    except:
        return []

def save_usernames(usernames):
    with open(usernames_file, "w") as f:
        json.dump(usernames, f, indent=2)

async def notify(entry):
    channel = bot.get_channel(FORUM_CHANNEL_ID)
    if not channel:
        print("❌ Salon forum introuvable")
        return

    tag = discord.utils.get(channel.available_tags, id=TAG_ID)
    if not tag:
        print("❌ Tag Letterboxd introuvable")
        return

    title = f"{entry['username']} posted a review"
    content = f"🎬 **{entry['title']}**\n⭐ {entry['rating']}\n🔗 {entry['url']}"

    embed = discord.Embed(
        title=entry['title'],
        description=f"Note : {entry['rating']}",
        url=entry['url'],
        color=0x00ff00
    )
    if entry['image']:
        embed.set_image(url=entry['image'])

    print(f"🚀 Création d’un thread pour {entry['title']}")
    await channel.create_thread(
        name=title,
        content=content,
        embed=embed,
        applied_tags=[tag]
    )

async def background_task():
    await bot.wait_until_ready()
    usernames = load_usernames()
    await watch_users(usernames, notify)

@bot.event
async def on_ready():
    print(f"✅ Bot connecté en tant que {bot.user.name}")
    bot.loop.create_task(background_task())

@bot.command(name="add")
async def add_user(ctx, username: str):
    usernames = load_usernames()
    if username in usernames:
        await ctx.send(f"⚠️ {username} est déjà surveillé.")
        return
    usernames.append(username)
    save_usernames(usernames)
    await ctx.send(f"✅ {username} ajouté à la liste. Redémarrage de la surveillance...")
    bot.loop.create_task(background_task())

@bot.command(name="list")
async def list_users(ctx):
    usernames = load_usernames()
    if not usernames:
        await ctx.send("📭 Aucun utilisateur surveillé pour l’instant.")
        return
    msg = "**📋 Utilisateurs surveillés :**\n" + "\n".join(f"- {u}" for u in usernames)
    await ctx.send(msg)

@bot.command(name="remove")
async def remove_user(ctx, username: str):
    usernames = load_usernames()
    if username not in usernames:
        await ctx.send(f"❌ {username} n’est pas dans la liste.")
        return
    usernames.remove(username)
    save_usernames(usernames)
    await ctx.send(f"✅ {username} a été retiré de la liste. Redémarrage de la surveillance...")
    bot.loop.create_task(background_task())

@bot.command(name="reload")
async def reload_watch(ctx):
    await ctx.send("🔁 Surveillance rechargée avec les utilisateurs actuels.")
    bot.loop.create_task(background_task())

bot.run(TOKEN)
