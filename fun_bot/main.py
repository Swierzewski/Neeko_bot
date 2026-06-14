from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path(__file__).parent / '.env')

import discord
from discord.ext import commands
from utils import make_embed
import comm_other
import comm_bot
import logging
import os
token = os.getenv('DISCORD_TOKEN')
DEEPL_AUTH_KEY = os.getenv('DEEPL_AUTH_KEY')

print("---START: Setup the Fun bot")
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot_prefix = '.'
bot = commands.Bot(command_prefix=bot_prefix, description=f'{bot_prefix}help for help', intents=intents)
print("---END : Setup the Fun bot")


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
async def error(ctx, *, message: str):
    await comm_bot.error(ctx, message=message)


@bot.group(invoke_without_command=True)
async def blocus(ctx):
    await comm_other.blocus(ctx)


@blocus.command(name="add")
async def add(ctx, url: str):
    await comm_other.add(ctx, url)


@bot.command()
async def trans(ctx, source_lang: str, target_lang: str, *, text: str):
    await comm_other.trans(ctx, source_lang, target_lang, text, DEEPL_AUTH_KEY)


@bot.command()
async def réussite(ctx):
    await comm_other.reussite(ctx)


@bot.command()
async def question(ctx, *, string):
    await comm_other.question(ctx, string=string)


@bot.command()
async def image(ctx, keyword: str):
    await comm_other.image(ctx, keyword)


@bot.command()
async def video(ctx, keyword: str):
    await comm_other.video(ctx, keyword)


@bot.command()
async def search(ctx, *, string):
    await comm_other.search_google_images(ctx, string)


@bot.command()
async def paypal(ctx):
    await ctx.send(
        embed=make_embed("SVP", "Pour le mariage, voici mon [paypal](https://paypal.me/swierzewski).", 0xECF22C))


bot.remove_command('help')


@bot.command()
async def help(ctx, category: str = None):
    await comm_bot.help(ctx, category, bot_prefix)


bot.run(token, log_handler=handler)
