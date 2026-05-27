

class TranscodingFailureException(Exception):
    

    def __init__(self, message:str, *args: object) -> None:
        """Exception thrown for any failure occuring during transcoding."""
        super().__init__(*args)

        self.exit_code = 1
        self.message = message