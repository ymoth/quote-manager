import ssl
import typing

import aiohttp
import requests


# Async function to download file
async def coroutine_download(url: str, **kwargs) -> bytes:
    current_session = aiohttp.ClientSession(
        connector=aiohttp.TCPConnector(ssl=ssl.SSLContext()),
        skip_auto_headers={"User-Agent"},
        raise_for_status=True,
        **kwargs
    )

    async with current_session.get(url) as file:
        return await file.read()


# Sync function to download file
def download(url: str) -> bytes:
    current_session = requests.Session()
    with current_session.get(url, allow_redirects=True) as file:
        return file.content
