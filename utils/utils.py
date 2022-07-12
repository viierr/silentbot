import httpx
import os

class utils:
    @staticmethod
    async def async_get(url: str):
        async with httpx.AsyncClient() as client:
            return await client.get(url)