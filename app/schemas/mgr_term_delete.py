"""管理员term删除"""

from app.rpc.async_http_client import api_request_model
from app.schemas.message import MessageModel


@api_request_model(api_name="/terms/mgr_term",
                   api_prefix="",
                   api_sufix="")
class MgrTermDeleteOut(MessageModel):
    """
    管理员term删除响应schema
    """
    pass
