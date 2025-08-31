import random
import httpx
from utils import *
import discord
import os
from ddgs import DDGS
import asyncio

async def question(ctx, string):
    random_ = random.randint(0,1000)
    print(random_)

    if ctx.message.author.id == 216198628094509056 and random_ > 900:
        await ctx.send(embed=make_embed(string, "tgl salope", 0xECF22C))
    else:
        if 25 >= random_ >= 0:
            await ctx.send(embed=make_embed(string, "tgl", 0xECF22C))
        elif 50 >= random_ >= 25:
            await ctx.send(embed=make_embed(string, "peut-être", 0xECF22C))
        elif 500 >= random_ >= 0:
            await ctx.send(embed=make_embed(string, "oui", 0xECF22C))
        elif 1000 >= random_ >= 500:
            await ctx.send(embed=make_embed(string, "non", 0xECF22C))


async def reussite(ctx):
    pourcentage = random.randint(1, 100)
    ret = f"{pourcentage}% de chance de réussir la session"
    await ctx.send(embed=make_embed("Réussite", ret, 0xECF22C))


async def trans(ctx, source_lang: str, target_lang: str, text: str, DEEPL_AUTH_KEY: str):
    url = 'https://api-free.deepl.com/v2/translate'
    headers = {'Authorization': f'DeepL-Auth-Key {DEEPL_AUTH_KEY}'}
    data = {'text': text, 'source_lang': source_lang.upper(), 'target_lang': target_lang.upper()}

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, data=data)
            response.raise_for_status()
            translation = response.json()['translations'][0]['text']
            await ctx.send(f"{translation}")
    except httpx.HTTPStatusError as e:
        await ctx.send(f"Error: {e.response.status_code} - {e.response.text}")
    except Exception as e:
        await ctx.send(f"An unexpected error occurred: {e}")



images_link = {
    "pussy": "micha.jpg",
    "toxic": "arnold_1.jpg",
    "toad": "marou.jpg",
    "czacio": "czacio.jpg",
    "donjuan": "adri_alpha.jpg",
    "pute": "vicpute.png",
    "louise": "adri.jpg",
    "kehbah": "axel.jpg",
    "karola": "czacio-2.jpg",
    "arbre": "arbre.jpg",
    "madison": "madison.jpg",
    "ester": "ester.jpg",
}


async def image(ctx, keyword: str):
    keyword = keyword.lower()

    if keyword in images_link:
        await ctx.send(file=discord.File(f'images/{images_link[keyword]}'))
    elif keyword == "salope":
        to_take = ["pussy", "karola", "kehbah", "pute", "toxic", "louise", "toad"]
        choosen = random.choice(to_take)
        await ctx.send(file=discord.File(f'images/{images_link[choosen]}'))
    else:
        await ctx.send(embed=make_embed("Error", "Keyword not found. Available keywords: " + ", ".join(images_link.keys()), 0xFF5733))


video_link = {
    "jlencule": "jlencule.mp4",
    "viol": "viol.mp4",
}


async def video(ctx, keyword: str):
    keyword = keyword.lower()

    if keyword in video_link:
        with open (f'images/{video_link[keyword]}', "rb") as video_file:
            video = discord.File(video_file)
        await ctx.send(file=video)
    else:     
        await ctx.send(embed=make_embed("Error", "Keyword not found. Available keywords: " + ", ".join(video_link.keys()), 0xFF5733))


async def blocus(ctx):
    gifs_never_give_up = load_gifs()
    await ctx.send(random.choice(gifs_never_give_up))


async def add(ctx, url: str):
    if not url.startswith(('http://', 'https://')) or not any(url.endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif', '.mp4']):
        await ctx.send(embed=make_embed("Error", "Please provide a valid image or video URL.", 0xFF5733))
        return
    
    gifs_never_give_up = load_gifs()
    if url in gifs_never_give_up:
        await ctx.send(embed=make_embed("Info", "This URL is already in the list.", 0x3498db))
        return

    gifs_never_give_up.append(url)
    save_gifs(gifs_never_give_up)
    await ctx.send(embed=make_embed("Success", "URL added to the list!", 0x2ecc71))


async def virus(ctx, member: discord.Member):
    file_path = "virus.exe"

    if not os.path.exists(file_path):
        await ctx.send("Error: File not found.")
        return

    embed = make_embed("Attention", "Salope n'installe pas le virus", 0xFF0000)

    try:
        await member.send(embed=embed)
        await member.send("", file=discord.File(file_path))
        await ctx.send(f"Sent the virus to {member.mention}.", delete_after=2)
    except discord.Forbidden:
        await ctx.send(f"Error: Cannot send DM to {member.mention}.")
    except Exception as e:
        await ctx.send(f"Error: {e}")


def _sync_image_search(query: str) -> str | None:
    try:
        with DDGS() as ddgs:
            results = list(ddgs.images(
                query=query,
                region= "fr-fr",
                safesearch= "off",
                max_results=1
            ))
            
            if results:
                return random.choice(results)['image']
    except Exception as e:
        print(f"Error during image search: {e}")
    return None

async def search_google_images(ctx, query: str) -> str | None:
    loop = asyncio.get_running_loop()
    
    image_url = await loop.run_in_executor(
        None,
        _sync_image_search,
        query
    )
    
    if not image_url:
        await ctx.send(embed=make_embed("Error", "Image not found.", 0xFF5733))
    
    await ctx.send(image_url)
