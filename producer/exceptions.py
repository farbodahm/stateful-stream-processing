class UserNotFoundError(ValueError):
    """Raise when no user found"""

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)
