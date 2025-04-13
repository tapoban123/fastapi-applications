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
