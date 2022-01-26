"""管理员内容编辑"""

from pydantic import BaseModel, Field

from app.rpc.async_http_client import api_request_model
from app.schemas.message import MessageModel


class MgrContentEditIn(BaseModel):
    """
    管理员内容编辑请求参数schemas
    """
    content_id: str = Field(None, title="内容ID", max_length=100)
    record_id: str = Field(None, title="记录ID", max_length=100)


class MgrContentEditOut(BaseModel):
    """
    管理员内容编辑响应参数schemas
    """
    content_id: str = Field(None, title="内容ID", max_length=100)
    record_id: str = Field(None, title="记录ID", max_length=100)


@api_request_model(api_name="/contents/mgr_content",
                   api_prefix="",
                   api_sufix="")
class MgrContentEditFinalOut(MessageModel):
    """
    管理员内容编辑响应参数schemas
    """
    detail: MgrContentEditOut = Field(None, title='')
