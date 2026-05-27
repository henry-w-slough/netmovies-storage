import uuid
import os
from typing import AsyncGenerator

import config

import Utility.MovieDataParser as MovieDataParser
import Utility.MovieDataTranscoder as MovieDataTranscoder


class MovieDataService:
    """Handles all direct logic relating to movie data."""


    async def upload_movie_data(self, storage_id:uuid.UUID, data_stream:AsyncGenerator[bytes, None]) -> uuid.UUID:

        movie_directory = os.path.join(config.MOVIE_ROOT_DIRECTORY, str(storage_id))
        os.makedirs(movie_directory, exist_ok=True)
        
        await MovieDataTranscoder.transcode_stream_to_directory(data_stream, movie_directory)

        return storage_id


    async def download_movie_data(self, storage_id:uuid.UUID) -> AsyncGenerator[bytes, None]:

        return MovieDataParser.stream_movie(os.path.join(config.MOVIE_ROOT_DIRECTORY, str(storage_id)))