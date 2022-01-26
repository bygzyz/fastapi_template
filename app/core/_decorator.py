from pydantic import BaseModel
from functools import wraps


class ErrorMessage(BaseModel):
    code: int
    message: str


class OpenAPIMethodDecorator():
    def __init__(self, code, message=""):
        self._code = code
        self._message = message

    def __call__(self, fn):
        def wrapper(*args, **kwargs):
            val = fn(*args, **kwargs)
            return dict({
                "model": ErrorMessage,
                "description": "Unauthorized",
                "content": {
                    "application/json":
                        {
                            "example": val
                        }
                }
            })

        return wrapper


@OpenAPIMethodDecorator
def openapi_error_func(code, message):
    return {"code": code, "message": message}


def open_api_doc_error(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        val = fn(*args, **kwargs)
        return dict({
            "model": ErrorMessage,
            "description": "Unauthorized",
            "content": {
                "application/json":
                    {
                        "example": val
                    }
            }
        })

    return wrapper


@open_api_doc_error
def openapi_doc_func(code, message):
    return {"code": code, "message": message}


def open_api_doc_class(cls):
    return dict(
        {"http_200_code_message": {
            "description": "OK",
            "content": {
                "application/json": {
                    "schema": cls.schema.schema()
                }
            }
        }
        })
