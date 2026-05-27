import ffmpeg
from typing import AsyncGenerator
import asyncio

import config


async def transcode_stream(data_stream:AsyncGenerator[bytes, None], chunk_size:int) -> AsyncGenerator[bytes, None]:


    transcode_process = (
        ffmpeg
        .input(data_stream)
        .output("pipe:0", vcodec=config.MOVIE_VCODEC, acodec=config.MOVIE_ACODEC, format=config.MOVIE_FILE_EXTENSION)
        .run_async(pipe_stdin=True)
    )


    async_loop = asyncio.get_event_loop()


    #iterating through each chunk of data in generator
    #note that we use run_in_executor to async transocde the process
    while chunk := await async_loop.run_in_executor(None, transcode_process.stdout.read, chunk_size):
        yield chunk
    

    #async waiting for ffmpeg to finish and release resources
    await async_loop.run_in_executor(None, transcode_process.wait)