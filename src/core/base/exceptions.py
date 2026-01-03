class AppError(Exception):
    DEFAULT_PUBLIC_MESSAGE = "An unexpected error occurred"

    def __init__(
        self,
        public_message: str | None = None,
        internal_message: str | None = None,
    ) -> None:
        self.public_message = public_message or self.DEFAULT_PUBLIC_MESSAGE
        self.internal_message = internal_message or self.public_message
        super().__init__(self.internal_message)


class ObjectNotFoundError(AppError):
    DEFAULT_PUBLIC_MESSAGE = "Requested object not found"


class CloudStorageProviderError(AppError):
    DEFAULT_PUBLIC_MESSAGE = "Cloud storage error"
