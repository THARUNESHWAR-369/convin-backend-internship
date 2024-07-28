from pydantic_settings import BaseSettings

class StatusCodes(BaseSettings):
    HTTP_OK: int = 200
    HTTP_CREATED: int = 201
    HTTP_BAD_REQUEST: int = 400
    HTTP_UNAUTHORIZED: int = 401
    HTTP_NOT_FOUND: int = 404
    HTTP_METHOD_NOT_ALLOWED: int = 405
    HTTP_INTERNAL_SERVER_ERROR: int = 500
    HTTP_SERVICE_UNAVAILABLE: int = 503
    HTTP_FORBIDDEN: int = 403

status_codes = StatusCodes()