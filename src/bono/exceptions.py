class ExistsError(ValueError):
    def __init__(self, message="A search filter with this name already exists."):
        super().__init__(message)