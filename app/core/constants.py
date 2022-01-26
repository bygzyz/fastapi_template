# -*- coding: UTF-8 -*-
from enum import Enum


class EnumProductType(str, Enum):
    any_share_cloud = 'any_share_cloud'
    any_backup_cloud = 'any_backup_cloud'
    any_robot_cloud = 'any_robot_cloud'


class EnumContentType(str, Enum):
    application = 'application'
    solution = 'solution'
    service = 'service'


class EnumRecordType(str, Enum):
    draft = 'draft'
    publish = 'publish'
    inherit = 'inherit'


class EnumTermType(str, Enum):
    tag = 'tag'
    group = 'group'


class EnumDeleteFlag(str, Enum):
    normal = '0'
    deleted = '1'


class EnumSortKey(str, Enum):
    created_date = 'created_date'
    product_type = 'product_type'
    content_id = 'content_id'
    record_id = 'record_id'
    content_name = 'content_name'
    publisher = 'publisher'
    description = 'description'
    content_type = 'content_type'
    sort_key = 'sort_key'
    version = 'version'


class EnumSortKeyMgrContents(str, Enum):
    """管理员一览检索 sort_key 限定"""
    created_date = 'created_date'
    updated_date = 'updated_date'
    product_type = 'product_type'
    content_id = 'content_id'
    record_id = 'record_id'
    content_name = 'content_name'
    publisher = 'publisher'
    sort_key = 'sort_key'
    description = 'description'
    content_type = 'content_type'
    version = 'version'
    ID = "ID"


class EnumSortKeyUserTerms(str, Enum):
    """用户Term一览检索 sort_key 限定"""
    created_date = 'created_date'
    updated_date = 'updated_date'
    product_type = 'product_type'
    term_id = 'content_id'
    sort_key = 'sort_key'
    slug = 'slug'
    text = 'text'
    ID = "ID"


class EnumSortType(str, Enum):
    asc = 'asc'
    desc = 'desc'


class EnumStatusType(str, Enum):
    init = 'init'
    release = 'release'
    cancel = 'cancel'


class EnumManagerPerPage(str, Enum):
    ten = "10"
    twenty = "20"
    fifty = "50"
    hundred = "100"
    more = "500"


class EnumUserPerPage(str, Enum):
    ten = "10"
    twenty = "20"
    fifty = "50"
    hundred = "100"


class ResponseSchema:
    def __init__(self, schema):
        self.schema = schema
        self.responses_200 = {
            "http_200_code_message": {
                "description": "OK",
                "content": {
                    "application/json": {
                        "schema": self.schema.schema()
                    }
                }
            }
        }
