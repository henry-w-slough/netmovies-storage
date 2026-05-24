import fastapi
import os
import uuid
import shutil

import config

from Exceptions.MovieNotFoundException import MovieNotFoundException


class MovieDirectoryController:


    def __init__(self, app:fastapi.FastAPI) -> None:
        """Handles all Movie directory related HTTP requests."""

        #adding endpoints to fastapi
        app.post("/directory/createMovie/{storageId:uuid}")(self.create_movie_directory)
        app.delete("/directory/deleteMovieByStorageId/{storageId:uuid}")(self.delete_movie_by_storage_id)


    async def create_movie_directory(self, storageId:uuid.UUID) -> fastapi.Response:

        #creating movie directory
        os.makedirs(os.path.join(config.MOVIE_ROOT_DIRECTORY, f"{storageId}"), exist_ok=True)

        return fastapi.responses.JSONResponse(status_code=201, content={"storageId": f"{storageId}"})
    
    
    async def delete_movie_by_storage_id(self, storageId:uuid.UUID) -> fastapi.Response:
        
        #creating movie directory
        movie_directory = os.path.join(config.MOVIE_ROOT_DIRECTORY, f"{storageId}")

        if not os.path.exists(movie_directory):
            raise MovieNotFoundException(f"Movie of StorageId: {storageId} could not be found within storage.")
        
        #deleting the directory
        shutil.rmtree(movie_directory)

        return fastapi.responses.Response(status_code=204)
    
        

    