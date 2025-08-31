import random
import asyncio
from duckduckgo_search import DDGS


def _sync_image_search(query: str) -> str | None:
    try:
        with DDGS() as ddgs:
            results = list(ddgs.images(
                keywords=query,
                region= "fr-fr",
                safesearch= "off",
                max_results=1
            ))
            
            if results:
                return random.choice(results)['image']
    except Exception as e:
        print(f"Error during image search: {e}")
    return None

async def search_google_images(query: str) -> str | None:
    loop = asyncio.get_running_loop()
    
    image_url = await loop.run_in_executor(
        None,
        _sync_image_search,
        query
    )
    
    if not image_url:
        print("No images found.")
    
    return image_url