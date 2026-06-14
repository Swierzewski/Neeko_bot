import discord
from discord.ext import commands
from pathlib import Path

from utils import make_embed
import comm_lol
import comm_bot

from dotenv import load_dotenv
import logging
import os

load_dotenv(Path(__file__).parent / '.env')
token = os.getenv('DISCORD_TOKEN')

print("---START: Setup the LoL bot")
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot_prefix = '.'
bot = commands.Bot(command_prefix=bot_prefix, description=f'{bot_prefix}help for help', intents=intents)
print("---END : Setup the LoL bot")


@bot.event
async def on_ready():
    print("Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print("------")


@bot.command()
async def hello(ctx):
    await comm_bot.hello(ctx)


@bot.command()
async def register(ctx, summoner: str, tag_line: str):
    await comm_bot.register(ctx, summoner, tag_line)


@bot.command()
async def profile(ctx):
    await comm_bot.profile(ctx)


@bot.command()
async def error(ctx, *, message: str):
    await comm_bot.error(ctx, message=message)


@bot.command()
async def unregister(ctx):
    await comm_bot.unregister(ctx)


@bot.command()
async def rank(ctx, *, summoner_input: str = None):
    await comm_lol.rank(ctx, summoner_input)


@bot.command()
async def lastgame(ctx, *, summoner_input: str = None):
    await comm_lol.lastgame(ctx, summoner_input)


@bot.command()
async def history(ctx, count: int = 5, *, summoner_input: str = None):
    await comm_lol.history(ctx, count, summoner_input=summoner_input)


@bot.command()
async def played(ctx, *, summoner_input: str = None):
    await comm_lol.played(ctx, summoner_input)


@bot.command()
async def streak(ctx, *, summoner_input: str = None):
    await comm_lol.streak(ctx, summoner_input)


@bot.command()
async def mastery(ctx, *, summoner_input: str = None):
    await comm_lol.mastery(ctx, summoner_input)


@bot.command()
async def livegame(ctx, *, summoner_input: str = None):
    await comm_lol.livegame(ctx, summoner_input)


bot.remove_command('help')


@bot.command()
async def help(ctx, category: str = None):
    await comm_bot.help(ctx, category, bot_prefix)


bot.run(token, log_handler=handler)
