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
        #returning a successful creation with the content of the service return
        return fastapi.responses.JSONResponse(status_code=201, content={"storageId": f"{await self.movie_directory_service.create_movie_directory(storage_id)}"})
    
    
    async def delete_movie_by_storage_id(self, storage_id:uuid.UUID) -> fastapi.Response:
        #not returning anything since a No Content, by name, has no content
        await self.movie_directory_service.delete_movie_by_storage_id(storage_id)
        return fastapi.responses.Response(status_code=204)
    
        

    