import uuid
import os
from typing import AsyncGenerator

import config

import Utility.MovieDataParser as MovieDataParser
import Utility.MovieDataTranscoder as MovieDataTranscoder


class MovieDataService:
    """Handles all direct logic relating to movie data."""


    async def upload_movie_data(self, storage_id:uuid.UUID, data_stream:AsyncGenerator[bytes, None]) -> uuid.UUID:

        #attaching the movie data stream in the connected movie directory using MovieDataAssembler
        await MovieDataParser.merge_stream(os.path.join(config.MOVIE_ROOT_DIRECTORY, str(storage_id)), data_stream)

        return storage_id


    async def download_movie_data(self, storage_id:uuid.UUID) -> AsyncGenerator[bytes, None]:
        
        stream = MovieDataParser.stream_movie(os.path.join(config.MOVIE_ROOT_DIRECTORY, str(storage_id)))

        return MovieDataTranscoder.transcode_stream(stream, 1024*1024*64)