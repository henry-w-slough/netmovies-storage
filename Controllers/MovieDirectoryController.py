import fastapi
import os
import uuid
import shutil

import config

from Exceptions.MovieNotFoundException import MovieNotFoundException
from Services import MovieDirectoryService


class MovieDirectoryController:


    def __init__(self, app:fastapi.FastAPI) -> None:
        """Handles and directs all Movie directory related HTTP requests."""

        self.movie_directory_service = MovieDirectoryService.MovieDirectoryService()

        #adding endpoints to fastapi
        app.post("/directory/createMovie/{storage_id:uuid}")(self.create_movie_directory)
        app.delete("/directory/deleteMovieByStorageId/{storage_id:uuid}")(self.delete_movie_by_storage_id)


    async def create_movie_directory(self, storage_id:uuid.UUID) -> fastapi.Response:
        #creating movie directory
        os.makedirs(os.path.join(config.MOVIE_ROOT_DIRECTORY, f"{storage_id}"), exist_ok=True)
        return fastapi.responses.JSONResponse(status_code=201, content={"storageId": f"{storage_id}"})
    
    
    async def delete_movie_by_storage_id(self, storage_id:uuid.UUID) -> fastapi.Response:
        
        #creating movie directory
        movie_directory = os.path.join(config.MOVIE_ROOT_DIRECTORY, f"{storage_id}")

        if not os.path.exists(movie_directory):
            raise MovieNotFoundException(f"Movie of StorageId: {storage_id} could not be found within storage.")
        
        #deleting the directory
        shutil.rmtree(movie_directory)

        return fastapi.responses.Response(status_code=204)
    
        

    