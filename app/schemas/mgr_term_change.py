"""管理员term修改"""

from typing import Optional

from pydantic import BaseModel, Field

from app.core.constants import EnumProductType, \
    EnumContentType
from app.rpc.async_http_client import api_request_model
from app.schemas.message import MessageModel


class MgrTermChangeIn(BaseModel):
    """
    管理员term修改请求schema
    """
    slug: Optional[str] = Field(None, title="slug", max_length=100)
    text: Optional[str] = Field(None, title="term文本", max_length=100)
    description: Optional[str] = Field(None, title="描述", max_length=100)
    sort_key: Optional[int] = Field(default=0, description="排序键")
    product_type: EnumProductType = Field(None, title="产品类别")
    content_type: EnumContentType = Field(None, title="内容类别")


@api_request_model(api_name="/terms/mgr_term",
                   api_prefix="",
                   api_sufix="")
class MgrTermChangeOut(MessageModel):
    """
    管理员term修改响应schema
    """
    pass
