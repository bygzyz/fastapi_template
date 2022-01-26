from app.schemas.message import MessageModel
from app.rpc.async_http_client import api_request_model

@api_request_model(api_name="/contents/contents_delete", api_prefix="",
                   api_sufix='')
class MgrContentDeleteResponse(MessageModel):
    pass
