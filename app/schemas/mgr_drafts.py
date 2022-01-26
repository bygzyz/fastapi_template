from pydantic import BaseModel, Field
from typing import List
from app.core.constants import EnumProductType, \
    EnumContentType
from app.rpc.async_http_client import api_request_model
from app.schemas.message import MessageModel


class SubDraft(BaseModel):
    product_type: EnumProductType = Field(None, title="产品类型")
    content_id: str = Field(None, max_length=100, title="内容ID")
    record_id: str = Field(None, max_length=100, title="记录ID")
    content_name: str = Field(None, max_length=50,
                              title="内容名称")
    content_type: EnumContentType = Field(None, title="内容类型")
    publisher: str = Field(None, max_length=50, title="发布者")
    created_date: str = Field(None, title="保存时间")


# 草稿一览输出参数schema
@api_request_model(api_name="/contents/drafts_list", api_prefix="",
                   api_sufix="")
class MgrDraft(BaseModel):
    # status: str = Field(..., min_length=1, max_length=100, title="状态")
    contents: List[SubDraft]
    page: int = Field(..., title="第几页")
    has_next: bool = Field(..., title="是否有下一页")
    total_pages: int = Field(..., title="总页数")
    count: int = Field(..., title="该页数据量")


class PagedDraft(MessageModel):
    pass
