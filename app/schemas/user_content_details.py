"""用户内容详细检索"""

from pydantic import BaseModel, Field

from app.core.constants import EnumProductType, \
    EnumContentType
from app.rpc.async_http_client import api_request_model
from app.schemas.message import MessageModel


class Content(BaseModel):
    """
    用户内容一览检索响应参数 schema
    """
    content_id: str = Field(None, title="内容ID", max_length=100)
    record_id: str = Field(None, title="记录ID", max_length=100)
    product_type: EnumProductType = Field(None, title="产品类别", max_length=50)
    content_name: str = Field(None, title="内容名称", max_length=50)
    publisher: str = Field(None, title="发布者", max_length=50)
    description: str = Field(None, title="描述", max_length=100)
    content_type: EnumContentType = Field(None, title="内容类别", max_length=50)
    version: str = Field(None, title="版本", max_length=10)
    product_info: str = Field(None, title="详细介绍", max_length=1000)
    logo_url: str = Field(None, title="logo地址", max_length=200)
    preview_media_urls: dict = Field(None, title="预览媒体地址")
    support_info: dict = Field(None, title="支持信息")
    count: int = Field(None, title="总件数")
    file_size: str = Field(None, title="文件大小")
    release_date: int = Field(None, title="发布时间")

class UserContentDetailsOut(BaseModel):
    """
    用户内容一览检索响应参数 schema
    """
    contents: Content = Field(None, title='')


@api_request_model(api_name="/contents/user_content_details",
                   api_prefix="",
                   api_sufix="")
class UserContentDetailsFinalOut(MessageModel):
    """
    用户内容一览检索响应参数 schema
    """
    detail: UserContentDetailsOut = Field(None, title='')
