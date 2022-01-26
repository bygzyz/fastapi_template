"""管理员草稿删除"""

from app.rpc.async_http_client import api_request_model
from app.schemas.message import MessageModel


@api_request_model(api_name="/contents/mgr_draft",
                   api_prefix="",
                   api_sufix="")
class MgrDraftDeleteOut(MessageModel):
    """
    管理员草稿删除响应参数schemas
    """
    pass
