import discord
import json


def make_embed(title, description="", color=0xECF22C, thumbnail_url=None, fields=None):
    embed = discord.Embed(title=title, description=description, color=color)

    if thumbnail_url:
        embed.set_thumbnail(url=thumbnail_url)
    
    if fields:
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

    return embed


def load_user_data():
    try:
        with open('users.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_user_data(data):
    with open('users.json', 'w') as f:
        json.dump(data, f, indent=4)


def load_feedback_data():
    try:
        with open('feedback.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_feedback_data(data):
    with open('feedback.json', 'w') as f:
        json.dump(data, f, indent=4)


def load_gifs():
    try:
        with open('gifs.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return [
            "https://i.gifer.com/1yMZ.gif", "https://c.tenor.com/cJ8vYM1EptoAAAAM/never-give.gif",
            "https://i.gifer.com/9FiC.gif", "https://tenor.com/2NRr.gif", "https://tenor.com/bDvPn.gif",
            "https://tenor.com/IzjI.gif", "https://tenor.com/beZfW.gif", "https://tenor.com/2KRq.gif",
            "https://tenor.com/bbsil.gif", "https://tenor.com/LuYC.gif"
        ]


def save_gifs(data):
    with open('gifs.json', 'w') as f:
        json.dump(data, f, indent=4)