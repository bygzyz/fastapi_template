"""用户内容一览检索"""

import math
from typing import Optional

from fastapi import APIRouter, Query, status, Request
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.logger import logger
from app.core._responses import ResponseSchema, \
    ResponseErrorSchema
from app.core._status_code import status_codes as sc, \
    trace_codes as tc
from app.rpc.async_http_client import APIClient
from app.schemas.user_contents import (
    UserContentsFinalOut,
    UserContentsPagedFinalOut,
)
from app.core.constants import (
    EnumContentType,
    EnumProductType,
    EnumSortType,
    EnumSortKey, EnumUserPerPage,
)

router = APIRouter()


@router.get(
    "/contents",
    response_model=UserContentsFinalOut,
    responses=dict([
        ResponseSchema(sc.OK, UserContentsFinalOut),
        ResponseErrorSchema(sc.BAD_REQUEST, tc.VALIDATION_102_ERROR),
    ])
)
async def user_contents(
        request: Request,
        product_type: EnumProductType = Query(None, description="产品类别"),
        content_type: EnumContentType = Query(None, description="内容分类"),
        group_slug: Optional[str] = Query(None,
                                          description="slug",
                                          max_length=100,
                                          ),
        content_text: Optional[str] = Query(None,
                                            description="可能是商品名称，作者，简介，标签",
                                            max_length=100,
                                            regex=r"^[-\w\s\u4E00-\u9FA5\uF900-\uFA2D]*$",
                                            ),
        publisher: Optional[str] = Query(None, description="作者",
                                         max_length=50,
                                         regex=r"^[-\w\s\u4E00-\u9FA5\uF900-\uFA2D]*$",
                                         ),
        page: int = Query(settings.PAGE,
                          description="页码",
                          ge=1,
                          le=settings.MAX_PAGE,
                          ),
        per_page: EnumUserPerPage = Query(EnumUserPerPage.ten,
                                          description="每页件数",
                                          ),
        sort_key: EnumSortKey = Query(default=EnumSortKey.sort_key,
                                      description="排序键",
                                      ),
        sort_type: EnumSortType = Query(default=EnumSortType.desc,
                                        description="排序类型",
                                        ),

):
    """
    # Description
    用户内容一览检索

    ## 参数说明
    参数名|参数说明|参数类型|参数位置|是否必须|备注|
    -|-|-|-|-|-
    product_type|产品类别|string|query|否|`['any_share_cloud','any_backup_cloud','any_robot_cloud']`
    content_type|内容分类|string|query|否|`['application', 'solution', 'service']`
    group_slug|slug|string|query|否|
    content_text|商品名称或作者或简介或标签|string|query|否|
    publisher|作者|string|query|否
    page|页码|int|query|否|
    per_page|每页件数|int|query|否|默认1000
    sort_key|排序键|string|query|否|
    sort_type|排序类型|string|query|否|
    """

    client = APIClient(request.app, UserContentsFinalOut)
    api_response = await client.retrieve(
        condition={
            'product_type': product_type.value if product_type else None,
            'content_type': content_type.value if content_type else None,
            'group_slug': group_slug,
            'content_text': content_text,
            'publisher': publisher,
        },
        extra_params={
            'page': page,
            'per_page': int(per_page),
            'sort_key': sort_key.value,
            'sort_type': sort_type.value.upper(),
        },
        paging_model=UserContentsPagedFinalOut
    )

    api_response_dict = api_response.dict()
    count = api_response_dict.get('detail').get('count')
    api_response_dict['detail']['page'] = page
    api_response_dict['detail']['has_next'] = page * int(per_page) < count
    api_response_dict['detail']['total_pages'] = math.ceil(
        count / int(per_page))
    logger.info("获取用户内容一览检索")
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=api_response_dict)
