from typing import List
from pydantic import BaseModel, Field, PositiveInt

from app.schemas.message import MessageModel
from app.core.constants import EnumProductType, \
    EnumContentType, EnumStatusType
from app.rpc.async_http_client import api_request_model


class SubContent(BaseModel):
    product_type: EnumProductType = Field(...,
                                          title="产品类型")
    content_id: str = Field(..., min_length=1, max_length=100,
                            regex=r"^[0-9a-z_]*$",
                            title="内容ID")
    record_id: str = Field(..., min_length=1, max_length=100,
                           regex=r"^[0-9a-z_]*$",
                           title="记录ID")
    content_name: str = Field(..., max_length=50, min_length=1,
                              title="内容名称")

    content_type: EnumContentType = Field(EnumContentType.application,
                                          title="产品类型")
    publisher: str = Field(..., max_length=50, min_length=1, title="发布者")
    status: EnumStatusType = Field(..., title="内容状态")
    release_date: str = Field(..., title="发布时间")
    release_manager: str = Field(..., max_length=100, min_length=1,
                                 title="发布者")
    cancel_date: str = Field(None, title="下架时间")
    cancel_manager: str = Field(None, max_length=100,
                                title="下架者")
    count: int = Field(None, title="下载次数")


# 管理员内容一览检索出例schema
@api_request_model(api_name="/contents/contents_list", api_prefix="",
                   api_suffix="")
class MgrContent(BaseModel):
    # status: str = Field(..., min_length=1, max_length=100, title="状态")
    contents: List[SubContent]
    page: PositiveInt = Field(..., title="第几页")
    has_next: bool = Field(..., title="是否有下一页")
    total_pages: int = Field(..., title="总页数")
    count: int = Field(..., title="该页数据量")


class PagedContent(MessageModel):
    pass
