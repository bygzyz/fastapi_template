"""管理员term新增"""

from typing import Optional

from pydantic import BaseModel, Field

from app.core.constants import EnumProductType, \
    EnumContentType
from app.rpc.async_http_client import api_request_model
from app.schemas.message import MessageModel


class ManagerTermAddIn(BaseModel):
    """
    管理员term新增响应参数
    """
    slug: str = Field(..., title="slug", min_length=1, max_length=100)
    text: str = Field(..., title="term文本", min_length=1, max_length=100)
    sort_key: Optional[int] = Field(default=0, title="排序键")
    description: Optional[str] = Field(...,
                                       title="描述",
                                       max_length=100)
    product_type: EnumProductType = Field(None, title="产品类别")
    content_type: EnumContentType = Field(None, title="内容类别")


@api_request_model(api_name="/terms/mgr_term",
                   api_prefix="",
                   api_sufix="")
class ManagerTermAddOut(MessageModel):
    """
    管理员term新增响应参数
    """
    pass
