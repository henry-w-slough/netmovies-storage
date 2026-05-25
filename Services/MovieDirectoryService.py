import uuid
import os
import shutil

import config

from Exceptions.MovieNotFoundException import MovieNotFoundException


class MovieDirectoryService:
    """Handles all logic relating to directories of movies."""


    async def create_movie_directory(self, storage_id:uuid.UUID) -> uuid.UUID:
        #creating movie directory
        os.makedirs(os.path.join(config.MOVIE_ROOT_DIRECTORY, f"{storage_id}"), exist_ok=True)
        
        return storage_id


    async def delete_movie_by_storage_id(self, storage_id:uuid.UUID) -> uuid.UUID:

        #creating movie directory
        movie_directory = os.path.join(config.MOVIE_ROOT_DIRECTORY, f"{storage_id}")

        if not os.path.exists(movie_directory):
            raise MovieNotFoundException(f"Movie of StorageId: {storage_id} could not be found within storage.")
        
        #deleting the directory
        shutil.rmtree(movie_directory)

        return storage_id