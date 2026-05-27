import ffmpeg
from typing import AsyncGenerator
import asyncio

import config
from Exceptions.TranscodingFailureException import TranscodingFailureException


async def transcode_stream_to_directory(data_stream:AsyncGenerator[bytes, None], directory:str):
    """Takes a data stream and transcodes it to the default extension type. The result is written directly to storage directory given."""
    
    #the ffmpeg arguments used to transcode and load the movie data stream
    process = await asyncio.create_subprocess_exec(
        #calling ffmpeg lib
        "ffmpeg",
        "-f", config.MOVIE_FILE_EXTENSION,
        #the input type, stdin stream
        "-i", "pipe:0",
        #codecs for video and audio
        "-c:v", "libx264",
        "-c:a", "aac",
        #override for existing directory without user input
        "-y",
        #ouput directory
        f"{directory}/{config.MOVIE_FILE_NAME}{config.MOVIE_FILE_EXTENSION}",
        #setting configuration to the pipeline created
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )


    #if stdin is none for the system, it means the pipe was never created to read from
    if process.stdin is None:
        raise TranscodingFailureException(f"FFmpeg movie transcoding to format: {config.MOVIE_FILE_EXTENSION} failed due to non-existing pipe.")
    

    #each chunk is ran through the transcoding process and written
    async for chunk in data_stream:
        process.stdin.write(chunk)
        await process.stdin.drain()


    #cleaning pipes (:<
    process.stdin.close()
    _, stderr_output = await process.communicate()


    #general exception for failure
    if process.returncode != 0:
        raise TranscodingFailureException(f"FFmpeg movie transcoding failed with output: {stderr_output.decode()}")