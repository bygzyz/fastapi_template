import math
from typing import Optional

from pydantic import PositiveInt
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Query, Depends, Request

from app.core.config import settings
from app.core.constants import EnumProductType, \
    EnumContentType, EnumManagerPerPage, EnumSortKeyMgrContents
from app.schemas.mgr_drafts import MgrDraft, PagedDraft
from app.core._status_code import status_codes as sc, \
    trace_codes as tc
from app.core._responses import ResponseErrorSchema
from app.rpc.async_http_client import APIClient
from app.core.esayAuth import get_exchange_user, \
    onetimetoken_reset

router = APIRouter()


@router.get("/contents/manager/draft",
            response_model=MgrDraft,
            responses=dict([
                ResponseErrorSchema(sc.BAD_REQUEST, tc.PARAM_ENTRY_101_ERROR),
                ResponseErrorSchema(sc.UNAUTHORIZED,
                                    tc.INVALID_USER_SESSION_106),
                ResponseErrorSchema(sc.FORBIDDEN, tc.AUTH_108_ERROR),
                ResponseErrorSchema(sc.INTERNAL_SERVER_ERROR,
                                    tc.INTERNAL_SERVER_112_ERROR)
            ])
            )
async def manager_draft(
        request: Request,
        access_token: str = Depends(get_exchange_user),
        product_type: Optional[EnumProductType] = Query(None, description=""),
        content_name: Optional[str] =
        Query(None, max_length=50, description="",
              regex=r"^[-\w\s\u4E00-\u9FA5\uF900-\uFA2D]*$"),
        publisher: Optional[str] =
        Query(None, max_length=50, description="",
              regex=r"^[-\w\s\u4E00-\u9FA5\uF900-\uFA2D]*$"),
        content_type: Optional[EnumContentType] = Query(None, description=""),
        save_date_from: Optional[str] = Query(None, description=""),
        save_date_to: Optional[str] = Query(None, description=""),
        sort_type: Optional[str] = Query('ASC', description="",
                                         max_length=100),
        page: Optional[int] = Query(settings.PAGE, description="", ge=1,
                                    le=settings.MAX_PAGE),
        per_page: EnumManagerPerPage = Query(EnumManagerPerPage.ten,
                                             description=""),
        sort_key: Optional[EnumSortKeyMgrContents] =
        Query(EnumSortKeyMgrContents.sort_key, description=""),
):
    """
    # Description
    管理员草稿一览检索

    ## Parameter 说明

    参数名 | 参数说明 | 参数类型 | 是否必须 | 备注
    - | - | - | - | -
    product_type | 产品类别 | string | 否 | 【any_share, any_backup, any_robot】
    content_type | 内容分类 | string | 否 | 【application, solution, service】
    content_name | 内容名称 | string | 否 |
    publisher | 发布者 | string | 否 |
    save_date_from | 发布日期起 | datetime | 否 |
    save_date_to | 发布日期止 | datetime | 否 |
    page | 指定页 | int | 否 | default = 1
    per_page | 每页数量 | int | 否 | default = 1000
    sort_key    | 排序键 | string | 否 | default = 'sort_key'
    sort_type    | 排序类别 | string | 否 | default = 'ASC'
    """

    client = APIClient(request.app, MgrDraft)

    api_response = await client.retrieve(
        opt_id=None,
        condition={
            "product_type": product_type.value
            if product_type is not None else None,
            "content_name": content_name,
            "publisher": publisher,
            "content_type": content_type.value
            if content_type is not None else None,
            "save_date_from": save_date_from,
            "save_date_to": save_date_to
        },
        extra_params={
            "page": page,
            "per_page": int(per_page),
            "sort_key": sort_key.value if sort_key is not None else None,
            "sort_type": sort_type,
        },
        paging_model=PagedDraft
    )

    response = PagedDraft()
    detail = getattr(api_response, 'detail', 0)
    response_model = MgrDraft.parse_obj(
        {
            "page": page,
            "has_next": page * int(per_page) < detail['count'],
            "total_pages": math.ceil(detail['count'] / int(per_page)),
            "count": detail['count'],
            "contents": detail['contents'],
        }
    )
    response.code = tc.SUCCESS
    response.message = tc.get_reason_phrase(tc.SUCCESS)
    response.detail = response_model.dict()

    return JSONResponse(
        status_code=sc.OK,
        content=response.dict(),
        headers={
            "x-onetimeToken": await onetimetoken_reset(request, access_token)}
    )
