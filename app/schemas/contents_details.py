from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field

from app.core.constants import EnumProductType, EnumContentType
from app.rpc.async_http_client import api_request_model
from app.schemas.message import MessageModel


class ContentsDetailsBase(BaseModel):
    content_id: Optional[str] = None
    old_record_id: str
    new_record_id: str


class ContentsDetailsCreate(BaseModel):
    content_id: str = Field(..., min_length=1, max_length=100,
                            title="内容ID", regex=r"^[0-9a-z_]*$")
    old_record_id: str = Field(..., min_length=1, max_length=100,
                               title="记录ID", regex=r"^[0-9a-z_]*$",
                               description="与该内容相同内容id的记录id")
    # new_record_id: str
    product_type: EnumProductType = Field(EnumProductType.any_share_cloud,
                                          title="产品类型")

    content_name: str = Field(..., max_length=50, min_length=1,
                              title="内容名称",
                              regex=r"^[-\w\s\u4E00-\u9FA5\uF900-\uFA2D]*$")
    publisher: str = Field(..., max_length=50, min_length=1, title="发布者",
                           regex=r"^[-\w\s\u4E00-\u9FA5\uF900-\uFA2D]*$")
    description: str = Field(..., max_length=100, min_length=1, title="内容描述")
    content_type: EnumContentType = Field(EnumContentType.application,
                                          title="内容类型")
    version: str = Field(..., min_length=1, max_length=10, title="内容版本")
    product_info: str = Field(..., min_length=1, max_length=1000,
                              title="产品信息")
    logo_url: str = Field(..., min_length=1, max_length=200, title="logo地址")
    thumbnail_url: str = Field(..., min_length=1, max_length=200,
                               title="缩略图地址")
    preview_media_urls: dict = Field(..., title="预览媒体地址")
    support_info: dict = Field(..., title="支持信息")
    file_id_list: List[str] = Field(..., min_items=1, title="文件ID",
                                    description="与该条内容相关的文件ID")
    tag_id_list: List[str] = Field(..., min_items=1, title="标签Id",
                                   description="与该内容相关的标签ID")
    group_id_list: List[str] = Field(..., min_items=1, title="组别ID",
                                     description="与该内容相关的组别ID")
    sort_key: int = Field(0, title="排序键", description="默认0")


class ContentsDetailsUpdate(BaseModel):
    pass


class SubFile(BaseModel):
    file_name: str = Field(..., min_length=1, max_length=100, title="文件名字")
    file_id: str = Field(..., min_length=1, max_length=100, title="文件ID")


class SubContent(BaseModel):
    content_id: str = Field(..., max_length=100, min_length=1, title="内容ID",
                            regex=r"^[0-9a-z_]*$")
    record_id: str = Field(..., max_length=100, min_length=1, title="记录ID",
                           regex=r"^[0-9a-z_]*$")
    product_type: EnumProductType = Field(..., title="产品类型",
                                          description="please choose product"
                                                      " type in the range")
    content_name: str = Field(..., max_length=50, min_length=1,
                              title="产品名称")
    publisher: str = Field(..., max_length=50, min_length=1, title="发布者")
    description: str = Field(..., max_length=100, min_length=1, title="描述")
    content_type: EnumContentType = Field(..., title="内容类型",
                                          description="")
    version: str = Field(..., max_length=10, min_length=1, title="内容版本")
    product_info: str = Field(..., max_length=1000, min_length=1,
                              title="产品信息")
    logo_url: str = Field(..., max_length=200, min_length=1, title="logo地址")
    thumbnail_url: str = Field(..., max_length=200, min_length=1,
                               title="缩略图地址")
    preview_media_urls: dict = Field(..., title="预览媒体地址")
    support_info: dict = Field(..., title="支持信息")
    file_list: List[SubFile] = Field(..., title="文件",
                                     description="与内容相关的文件")


# 内容详细输出schema
@api_request_model(api_name="/contents/content_detail", api_prefix="",
                   api_sufix="")
class ContentDetailResponseModel(MessageModel):
    pass


class ContentDetailModel(BaseModel):
    status: str = Field(..., max_length=100, min_length=1, title="状态")
    content: SubContent


class DraftDetailsCreate(BaseModel):
    content_id: str = Field(..., max_length=100, min_length=1, title="内容ID",
                            regex=r"^[0-9a-z_]*$")
    old_record_id: str = Field(..., max_length=100, min_length=1,
                               title="记录ID", regex=r"^[0-9a-z_]*$",
                               description="表中同内容ID的记录ID")
    product_type: EnumProductType = Field(EnumProductType.any_share_cloud,
                                          title="产品类型")
    content_name: str = Field(..., max_length=50, min_length=1,
                              title="内容名称",
                              regex=r"^[-\w\s\u4E00-\u9FA5\uF900-\uFA2D]*$")

    publisher: Optional[str] = \
        Field(None, max_length=50, title="发布者",
              regex=r"^[-\w\s\u4E00-\u9FA5\uF900-\uFA2D]*$")

    description: Optional[str] = Field(None, max_length=100,
                                       title="草稿描述")
    content_type: Optional[EnumContentType] = Field(None, title="内容类型")
    version: Optional[str] = Field(None, max_length=10, title="内容版本")
    product_info: Optional[str] = Field(None, max_length=1000, title="产品信息")
    logo_url: Optional[str] = Field(None, max_length=200, title="logo地址")
    thumbnail_url:  Optional[str] = Field(None, max_length=200,
                                          title="缩略图地址")
    preview_media_urls: Optional[dict] = Field(None, title="预览媒体地址")
    sort_key: Optional[int] = Field(1, title="排序键")
    support_info: Optional[dict] = Field(None, title="支持信息")
    file_id_list: Optional[List[str]] = Field([], title="文件ID",
                                              description="与内容相关的文件ID")
    tag_id_list: Optional[List[str]] = Field([], title="标签ID",
                                             description="与内容相关的标签ID")
    group_id_list:  Optional[List[str]] = Field([], title="组别ID",
                                                description="与内容相关的组别ID")


@api_request_model(api_name="contents", api_prefix="",
                   api_sufix='contents_delete')
class Simple(BaseModel):
    code: int = Field(200, title="状态码")
    status: str = Field(..., min_length=1, max_length=100,  title="状态")
