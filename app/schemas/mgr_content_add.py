"""管理员内容新增"""

from pydantic import BaseModel, Field

from app.rpc.async_http_client import api_request_model
from app.schemas.message import MessageModel


class MgrContentAddOut(BaseModel):
    """
    管理员内容新增响应参数schemas
    """
    content_id: str = Field(None, title="内容ID", max_length=100)
    record_id: str = Field(None, title="记录ID", max_length=100)


@api_request_model(api_name="/contents/mgr_content",
                   api_prefix="",
                   api_sufix="")
class MgrContentAddFinalOut(MessageModel):
    """
    管理员内容新增响应参数schemas
    """
    detail: MgrContentAddOut = Field(None, title='')
