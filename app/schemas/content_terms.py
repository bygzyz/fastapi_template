"""内容term检索"""

from typing import List

from pydantic import BaseModel, Field

from app.core.constants import EnumTermType
from app.rpc.async_http_client import api_request_model
from app.schemas.message import MessageModel


class Terms(BaseModel):
    """
    内容term检索响应参数
    """
    term_id: str = Field(None, title="termID", max_length=100)
    slug: str = Field(None, title="slug", max_length=100)
    text: str = Field(None, title="term文本", max_length=100)
    description: str = Field(None, title="描述", max_length=100)


class Relations(BaseModel):
    """
    内容term检索响应参数
    """
    record_id: str = Field(None, title="记录ID", max_length=100)
    term_type: EnumTermType = Field(None, title="term类型", max_length=50)
    terms: List[Terms] = Field(None, title="")


class ContentTermsOut(BaseModel):
    """
    内容term检索响应参数
    """
    relations: Relations = Field(None, title="")


@api_request_model(api_name="/contents/content_terms",
                   api_prefix="",
                   api_sufix="")
class ContentTermsFinalOut(MessageModel):
    """
    内容term检索响应参数
    """
    detail: ContentTermsOut = Field(None, title='')
