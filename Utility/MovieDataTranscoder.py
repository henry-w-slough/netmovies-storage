import ffmpeg
import tempfile
import os
from typing import AsyncGenerator

import config



def transcode_byte_stream(byte_stream:AsyncGenerator[bytes, None], movie_dir:str) -> None:
    print(byte_stream)


