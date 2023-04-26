class NotFoundError(ValueError):
    """Base class fot rasing when there aren't any resource found"""

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class UserNotFoundError(NotFoundError):
    """Raise when no user is found"""

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class TweetNotFoundError(NotFoundError):
    """Raise when no tweet is found"""

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class ProtobufSerializerNotFoundError(NotFoundError):
    """Raise when no serializer is found"""

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class ModelGeneratorFunctionNotFoundError(NotFoundError):
    """Raise when no model generator function is found"""

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class ProtobufDeserializerNotFound(NotFoundError):
    """Raise when no deserializer is found"""

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)
