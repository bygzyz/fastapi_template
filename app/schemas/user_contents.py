"""用户内容一览检索"""

from typing import List

from pydantic import BaseModel, Field

from app.core.constants import EnumProductType, \
    EnumContentType
from app.rpc.async_http_client import api_request_model
from app.schemas.message import MessageModel


class Contents(BaseModel):
    """
    用户内容一览检索请求参数 schema
    """
    product_type: EnumProductType = Field(None, title="产品类别", max_length=50)
    content_id: str = Field(None, title="内容ID", max_length=100)
    record_id: str = Field(None, title="记录ID", max_length=100)
    content_name: str = Field(None, title="内容名称", max_length=50)
    publisher: str = Field(None, title="发布者", max_length=50)
    description: str = Field(None, title="描述", max_length=100)
    content_type: EnumContentType = Field(None, title="内容类别", max_length=50)
    version: str = Field(None, title="版本", max_length=10)
    thumbnail_url: str = Field(None, title="缩略图", max_length=200)


class UserContentsOut(BaseModel):
    """
    用户内容一览检索响应参数 schema
    """
    page: int = Field(None, title='页码')
    has_next: bool = Field(None, title='是否有下一页')
    total_pages: int = Field(None, title='总页码')
    count: int = Field(None, title='总件数')
    contents: List[Contents] = Field(None, title='')


class UserContentsPagedOut(BaseModel):
    """
    用户内容一览检索响应分页参数 schema
    """
    count: int = Field(None, title='总件数')
    contents: List[Contents] = Field(None, title='')


class UserContentsPagedFinalOut(MessageModel):
    """
    用户内容一览检索响应分页参数 schema
    """
    detail: UserContentsPagedOut = Field(None, title='')


@api_request_model(api_name="/contents/user_contents",
                   api_prefix="",
                   api_sufix="")
class UserContentsFinalOut(MessageModel):
    """
    用户内容一览检索响应参数 schema
    """
    detail: UserContentsOut = Field(None, title='')
