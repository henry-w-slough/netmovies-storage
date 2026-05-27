import ffmpeg
from typing import AsyncGenerator
import asyncio

import config


async def transcode_stream_to_directory(data_stream:AsyncGenerator[bytes, None], directory:str):
    """Takes a data stream and transcodes it to the default extension type. The result is written directly to storage directory given."""
    
    #the ffmpeg arguments used to transcode and load the movie data stream
    process = await asyncio.create_subprocess_exec(
        #calling ffmpeg lib
        "ffmpeg",
        "-f", config.MOVIE_FILE_FORMAT,
        "-probesize", "2147483647",
        "-analyzeduration", "2147483647",
        #the input type, stdin stream
        "-i", "pipe:0",
        #codecs for video and audio
        "-c:v", config.MOVIE_VCODEC,
        "-c:a", config.MOVIE_ACODEC,
        #override for existing directory without user input
        "-y",
        #movflags for mp4 file format default
        "-movflags", "faststart",
        #ouput directory
        f"{directory}/{config.MOVIE_FILE_NAME}.{config.MOVIE_FILE_FORMAT}",
        #setting configuration to the pipeline created
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )


    if process.stdin is None:
        raise Exception("Exception thrown when transcoding, pipe is invalid or not created.")
    

    #catching BrokenPipeError allows ffmpeg to continue without first moov
    try:
        #each chunk is ran through the transcoding process and written
        async for chunk in data_stream:
            process.stdin.write(chunk)
            await process.stdin.drain()
            
    except BrokenPipeError:
        print("WARNING: Pipe broken during transcoding write process.")
        pass


    #cleaning pipes (:<
    process.stdin.close()
    _, stderr_output = await process.communicate()


    #general exception for failure
    if process.returncode != 0:
        raise Exception(f"FFmpeg movie transcoding failed with output: {stderr_output.decode()}")