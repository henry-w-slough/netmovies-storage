import fastapi
import uuid
import os

from Utility import MovieDataParser
import config


class MovieDataController:


    def __init__(self, app:fastapi.FastAPI) -> None:
        """Handles all Movie data related HTTP requests."""
        #adding endpoints to fastapi
        app.post("/data/uploadMovieData/{storageId:uuid}")(self.uploadMovieData)
        app.get("/data/downloadMovieData/{storageId:uuid}")(self.downloadMovieData)


    async def uploadMovieData(self, storageId:uuid.UUID, request:fastapi.Request) -> fastapi.Response:

        movie_directory = os.path.join(config.MOVIE_ROOT_DIRECTORY, str(storageId))

        #attaching the movie data stream in the movie directory using MovieDataAssembler
        await MovieDataParser.merge_stream(movie_directory, request.stream())

        return fastapi.responses.JSONResponse(
            status_code=200,
            content={"storageId": str(storageId)}
        )


    async def downloadMovieData(self, storageId:uuid.UUID) -> fastapi.Response:

        return fastapi.responses.StreamingResponse(
            status_code=200,
            content=MovieDataParser.stream_movie(f"{config.MOVIE_ROOT_DIRECTORY}/{storageId}/{config.MOVIE_FILE_NAME}"),
            headers={"fileName": config.MOVIE_FILE_NAME, "fileExtension": config.MOVIE_FILE_EXTENSION} 
        )