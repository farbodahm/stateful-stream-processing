class UserNotFoundError(ValueError):
    """Raise when no user is found"""

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class TweetNotFoundError(ValueError):
    """Raise when no tweet is found"""

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class ProtobufSerializerNotFoundError(ValueError):
    """Raise when no serializer is found"""

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class ModelGeneratorFunctionNotFoundError(ValueError):
    """Raise when no model generator function is found"""

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)
