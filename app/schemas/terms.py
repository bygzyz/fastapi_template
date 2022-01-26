from typing import List
from pydantic import BaseModel, Field, PositiveInt
from app.core.constants import EnumTermType, \
    EnumContentType, EnumProductType
from app.rpc.async_http_client import api_request_model
from app.schemas.message import MessageModel


class Terms(BaseModel):
    search_tag_text: str = Field(..., min_length=1, max_length=100,
                                 title="标签文本")


class TermD(BaseModel):
    term_id: str = Field(..., min_length=1, max_length=100, title="标签ID")
    slug: str = Field(..., min_length=1, max_length=100, title="slug")
    text: str = Field(..., min_length=1, max_length=100, title="标签文本")
    description: str = Field(..., min_length=1, max_length=100, title="标签描述")
    product_type: EnumProductType = Field(None, title="产品类型")
    content_type: EnumContentType = Field(None, title="内容类型")


@api_request_model(api_name="/term/term_list_get", api_prefix="", api_sufix="")
class Term(BaseModel):
    """
    Term一览响应model
    """
    # status: str = Field(..., min_length=1, max_length=100, title="返回状态")
    term_type: EnumTermType = Field(..., min_length=1, max_length=100,
                                    title="term类型")
    terms: List[TermD]
    page: PositiveInt = Field(..., title="第几页")
    has_next: bool = Field(..., title="是否有下一页")
    total_pages: int = Field(..., title="总页数")
    count: int = Field(..., title="该页数据量")


class PagedTerm(MessageModel):
    pass
