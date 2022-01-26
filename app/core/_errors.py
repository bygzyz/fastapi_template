from pydantic import BaseModel
from omi_async_http_client import HTTPException
from typing import Any, Type

from app.core._status_code import TraceCode, StatuCode


class ErrorMessage(BaseModel):
    code: int
    message: str


class HTTPAPIException(HTTPException):
    def __init__(
            self, trace_code: int,
            status_code: int = StatuCode.INTERNAL_SERVER_ERROR,
            detail: Any = None,
            headers: dict = None
    ) -> None:
        super().__init__(status_code=status_code, detail=detail,
                         headers=headers)
        self.trace_code = trace_code

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f"{class_name}(status_code={self.status_code!r}," \
               f"trace_code={self.trace_code!r},detail={self.detail!r}) "

    def to_openapi_schema(self) -> dict:
        return self.openapi_schema(ErrorMessage, self.status_code,
                                   self.trace_code)

    @classmethod
    def schema_from_code(cls,
                         status_code: StatuCode,
                         trace_code: TraceCode
                         ) -> dict:
        return cls.openapi_schema(ErrorMessage, status_code, trace_code)

    @classmethod
    def openapi_schema(cls,
                       model: Type[BaseModel],
                       status_code: StatuCode,
                       trace_code: TraceCode
                       ) -> dict:
        return dict(
            {
                "model": model,
                "description": StatuCode.get_reason_phrase(status_code),
                "content": {
                    "application/json":
                        {
                            "schema": model.schema(),
                            "example": {
                                "code": trace_code,
                                "message": TraceCode.get_reason_phrase(
                                    trace_code)
                            }
                        }
                }
            }
        )


def api_exception_decorator(**kwargs):
    def decorator(cls):
        for key, val in kwargs.items():
            if val is not None:
                setattr(cls, key, val)  # key -> _key for internal use
        return cls

    return decorator


@api_exception_decorator(status_code=StatuCode.BAD_REQUEST,
                         trace_code=TraceCode.PARAM_ENTRY_101_ERROR)
class ParamEntryError(HTTPAPIException):
    pass


@api_exception_decorator(status_code=StatuCode.FORBIDDEN,
                         trace_code=TraceCode.AUTH_108_ERROR)
class AuthError(HTTPAPIException):
    pass


@api_exception_decorator(status_code=StatuCode.NOT_FOUND,
                         trace_code=TraceCode.DATA_NOT_FOUND_109)
class DataNotFoundError(HTTPAPIException):
    pass


@api_exception_decorator(status_code=StatuCode.NOT_FOUND,
                         trace_code=TraceCode.DATA_NOT_FOUND_109)
class OidcCallBackError(HTTPAPIException):
    pass
