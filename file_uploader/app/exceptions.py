from fastapi import HTTPException, status


class AuthExceptions(HTTPException):
    """Base Exception for Auth Errors."""

    pass


class AccountNotFoundError(AuthExceptions):
    def __init__(self):
        message = "Account not found."
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=message)


class InvalidCredentialsError(AuthExceptions):
    def __init__(self):
        message = "Invalid User Credentials."
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=message)


class UserValidationFailedError(AuthExceptions):
    def __init__(self):
        message = "Failed to validate user."
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=message)


class AccessTokenInvalidError(AuthExceptions):
    def __init__(self):
        message = "Invalid Access Token."
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=message)


class UserAlreadyExistsError(AuthExceptions):
    def __init__(self):
        message = "Account already exists with that email id."
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=message)


class FileUploadServiceExceptions(HTTPException):
    """Base Exception for File Upload Service Errors."""
    pass


class FileSizeMoreThan5MBError(FileUploadServiceExceptions):
    def __init__(self):
        message = "File size must not exceed 5 MB."
        super().__init__(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail=message)


class DuplicateAssetNameError(FileUploadServiceExceptions):
    def __init__(self):
        message = "Resource ID must be unique."
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=message)
