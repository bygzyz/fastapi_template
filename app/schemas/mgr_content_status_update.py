from pydantic import BaseModel, Field

from app.schemas.message import MessageModel
from app.rpc.async_http_client import api_request_model
from app.core.constants import EnumStatusType


@api_request_model(api_name="/contents/contents_status", api_prefix="",
                   api_sufix='')
class MgrContentStatusUpdateResponse(MessageModel):
    pass


class MgrStatusUpdate(BaseModel):
    status: EnumStatusType = Field(..., title="状态")
    update_status: EnumStatusType = Field(...,
                                          title="更新状态",
                                          description="改变之后的状态")
