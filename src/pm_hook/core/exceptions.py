class AppError(Exception):
    def __init__(
        self,
        message: str,
        code: str,
        status_code: int = 400
    ):
        self.message = message
        self.code = code
        self.status_code = status_code

        super().__init__(message)
        


# usage example: 
#     if len(playlist.tracks) >= 30:


#     raise AppError(
#         message="Playlist is full",
#         code="PLAYLIST_FULL",   # ← stable, machine-readable
#         status_code=409,
#     )
