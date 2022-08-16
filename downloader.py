import ssl
import typing

import aiohttp
import requests

CurrentSession = typing.TypeVar("CurrentSession", bound=typing.Union[aiohttp.ClientSession, requests.Session])


def get_session(session_type: typing.Type[CurrentSession], **kwargs) -> CurrentSession:
    if isinstance(session_type, aiohttp.ClientSession):
        return aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(ssl=ssl.SSLContext()),
            skip_auto_headers={"User-Agent"},
            raise_for_status=True,
            **kwargs
        )
    else:
        return requests.Session()


# Async function to download file
async def coroutine_download(url: str) -> bytes:
    current_session = get_session(aiohttp.ClientSession)
    async with current_session.get(url) as file:
        return await file.read()


# Sync function to download file
def download(url: str) -> bytes:
    current_session = get_session(requests.Session)
    with current_session.get(url, allow_redirects=True) as file:
        return file.content
