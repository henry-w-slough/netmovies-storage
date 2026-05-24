import aiofiles
import os
from typing import AsyncGenerator

import config


async def merge_stream(directory:str, data_stream:AsyncGenerator[bytes, None]) -> None:
    """Takes a data stream from HTTP and connects it, outputting the connected file to the given directory."""
    #opening the new file
    async with aiofiles.open(os.path.join(directory, f"{config.MOVIE_FILE_NAME}"), "wb") as file:
        #writing the data stream, note that it will write as the data is received
        async for chunk in data_stream:
            await file.write(chunk)


async def stream_movie(src: str):
    """Yields movie data in chunks from the given source path."""
    async with aiofiles.open(src, "rb") as file:
        while chunk := await file.read(config.READ_SIZE):
            yield chunk



