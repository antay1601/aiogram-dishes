import httpx
from config import PEXELS_API_KEY

async def get_image_url(query: str) -> str | None:
    """
    Ищет изображение на Pexels и возвращает URL первого найденного.
    """
    if not PEXELS_API_KEY:
        print("PEXELS_API_KEY не найден.")
        return None

    headers = {
        "Authorization": PEXELS_API_KEY
    }
    
    url = f"https://api.pexels.com/v1/search"
    params = {
        "query": query,
        "per_page": 1,
        "page": 1
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            if data["photos"]:
                # Возвращаем URL среднего размера
                return data["photos"][0]["src"]["medium"]
            else:
                print(f"Изображения по запросу '{query}' не найдены.")
                return None
    except httpx.HTTPStatusError as e:
        print(f"Ошибка запроса к Pexels API: {e.response.status_code} - {e.response.text}")
        return None
    except Exception as e:
        print(f"Произошла ошибка при работе с Pexels API: {e}")
        return None

if __name__ == '__main__':
    import asyncio

    async def test():
        query = "Pasta Carbonara"
        url = await get_image_url(query)
        if url:
            print(f"Найден URL для '{query}': {url}")
        else:
            print(f"Не удалось найти URL для '{query}'.")

    asyncio.run(test())
