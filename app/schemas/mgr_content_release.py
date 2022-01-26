from app.schemas.message import MessageModel
from app.rpc.async_http_client import api_request_model

@api_request_model(api_name="/contents/release", api_prefix="",
                   api_sufix='')
class MgrContentReleaseResponse(MessageModel):
    pass
