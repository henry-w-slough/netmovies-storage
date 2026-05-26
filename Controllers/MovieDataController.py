import fastapi
import uuid
import os

from Utility import MovieDataParser
from Utility import MovieDataTranscoder
from Services import MovieDataService
import config


class MovieDataController:


    def __init__(self, app:fastapi.FastAPI) -> None:
        """Handles all Movie data related HTTP requests."""

        self.movie_data_service = MovieDataService.MovieDataService()

        #adding endpoints to fastapi
        app.post("/data/uploadMovieData/{storage_id:uuid}")(self.upload_movie_data)
        app.get("/data/downloadMovieData/{storage_id:uuid}")(self.download_movie_data)


    async def upload_movie_data(self, storage_id:uuid.UUID, request:fastapi.Request) -> fastapi.Response:
        
        #storageId in content is a string in order to 
        return fastapi.responses.JSONResponse(
            status_code=200,
            content={"storageId": str(await self.movie_data_service.upload_movie_data(storage_id, request.stream()))}
        )


    async def download_movie_data(self, storage_id:uuid.UUID) -> fastapi.Response:

        return fastapi.responses.StreamingResponse(
            status_code=200,
            content = await self.movie_data_service.download_movie_data(storage_id),
            headers={"fileName": config.MOVIE_FILE_NAME, "fileExtension": config.MOVIE_FILE_EXTENSION} 
        )