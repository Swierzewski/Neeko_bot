import random
import httpx
from utils import make_embed, load_gifs, save_gifs
import discord
import os
from ddgs import DDGS
import asyncio
from ollama import AsyncClient as OllamaClient

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

_OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'llama3.2:1b')

with open(os.path.join(BASE_DIR, 'prompt.md'), 'r', encoding='utf-8') as _f:
    _SYSTEM_PROMPT = _f.read()


async def question(ctx, string):
    async with ctx.typing():
        try:
            client = OllamaClient()
            response = await client.chat(
                model=_OLLAMA_MODEL,
                messages=[
                    {'role': 'system', 'content': _SYSTEM_PROMPT},
                    {'role': 'user', 'content': string},
                ],
            )
            answer = response.message.content.strip()
        except Exception as e:
            print(f"Ollama error: {e}")
            answer = "My brain short-circuited. Try again, you impatient clown."

    await ctx.send(embed=make_embed(string, answer, 0xECF22C))


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
        await ctx.send(file=discord.File(os.path.join(BASE_DIR, 'images', images_link[keyword])))
    elif keyword == "salope":
        choosen = random.choice(["pussy", "karola", "kehbah", "pute", "toxic", "louise", "toad"])
        await ctx.send(file=discord.File(os.path.join(BASE_DIR, 'images', images_link[choosen])))
    else:
        await ctx.send(embed=make_embed("Error", "Keyword not found. Available keywords: " + ", ".join(images_link.keys()), 0xFF5733))


video_link = {
    "jlencule": "jlencule.mp4",
    "viol": "viol.mp4",
}


async def video(ctx, keyword: str):
    keyword = keyword.lower()

    if keyword in video_link:
        with open(os.path.join(BASE_DIR, 'images', video_link[keyword]), "rb") as video_file:
            await ctx.send(file=discord.File(video_file))
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


def _sync_image_search(query: str) -> str | None:
    try:
        with DDGS() as ddgs:
            results = list(ddgs.images(
                query=query,
                region="fr-fr",
                safesearch="off",
                max_results=20,
            ))
            if results:
                return random.choice(results)['image']
    except Exception as e:
        print(f"Error during image search: {e}")
    return None


async def search_google_images(ctx, query: str):
    loop = asyncio.get_running_loop()

    image_url = await loop.run_in_executor(None, _sync_image_search, query)

    if not image_url:
        await ctx.send(embed=make_embed("Error", "Image not found.", 0xFF5733))
        return

    await ctx.send(image_url)
