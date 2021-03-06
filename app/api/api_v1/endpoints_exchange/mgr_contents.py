import math
from typing import Optional

from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import JSONResponse
from pydantic import PositiveInt

from app.core.config import settings
from app.core.constants import EnumProductType, \
    EnumContentType, EnumStatusType, EnumManagerPerPage, EnumSortKeyMgrContents
from app.schemas.mgr_contents import MgrContent, PagedContent
from app.core._responses import ResponseErrorSchema
from app.core._status_code import status_codes as sc, \
    trace_codes as tc
from app.rpc.async_http_client import APIClient
from app.core.esayAuth import get_exchange_user, \
    onetimetoken_reset

router = APIRouter()


@router.get("/contents/manager/publish",
            response_model=MgrContent,
            responses=dict([
                ResponseErrorSchema(sc.BAD_REQUEST, tc.PARAM_ENTRY_101_ERROR),
                ResponseErrorSchema(sc.UNAUTHORIZED,
                                    tc.INVALID_USER_SESSION_106),
                ResponseErrorSchema(sc.FORBIDDEN, tc.AUTH_108_ERROR),
                ResponseErrorSchema(sc.INTERNAL_SERVER_ERROR,
                                    tc.INTERNAL_SERVER_112_ERROR)
            ]))
async def manager_search_content(
        request: Request,
        access_token: str = Depends(get_exchange_user),
        product_type: Optional[EnumProductType] = Query(None, description=""),
        content_type: Optional[EnumContentType] = Query(None, description=""),
        content_name: Optional[str] =
        Query(None, max_length=50, description="",
              regex=r"^[-\w\s\u4E00-\u9FA5\uF900-\uFA2D]*$"),
        publisher: Optional[str] =
        Query(None, max_length=50, description="",
              regex=r"^[-\w\s\u4E00-\u9FA5\uF900-\uFA2D]*$"),
        status: Optional[EnumStatusType] = Query(None, description=""),
        release_manager: Optional[str] = Query(None, max_length=100,
                                               description=""),
        release_date_from: Optional[str] = Query(None, description=""),
        release_date_to: Optional[str] = Query(None, description=""),
        cancel_date_from: Optional[str] = Query(None, description=""),
        cancel_date_to: Optional[str] = Query(None, description=""),
        page: Optional[int] = Query(settings.PAGE, description="", ge=1,
                                    le=settings.MAX_PAGE),
        per_page: EnumManagerPerPage = Query(EnumManagerPerPage.ten,
                                             description=""),
        sort_key: Optional[EnumSortKeyMgrContents] =
        Query(EnumSortKeyMgrContents.sort_key, description=""),
        sort_type: Optional[str] = Query('ASC', description="", max_length=100)
):
    """

    # Description
    ???????????????????????????

    ## Parameter ??????

    ????????? | ???????????? | ???????????? | ???????????? |??????
    -|-|-|-|-
    product_type | ???????????? | string | ??? | ???any_share, any_backup, any_robot???
    content_type | ???????????? | string | ??? | ???application, solution, service???
    content_name | ???????????? | string | ??? |
    publisher    | ?????????   | string | ??? |
    status       | ??????    | string| ??? |  ???init, release, stop???
    release_manager | ????????? | string | ??? |
    release_date_from | ??????????????? | datetime | ??? |
    release_date_to | ??????????????? | datetime| ??? |
    cancel_date_from | ??????????????? | datetime | ??? |
    cancel_date_to | ??????????????? | datetime| ??? |
    page          | ????????? | int | ??? | default = 1
    per_page     |  ???????????? | int | ??? | default = 1000
    sort_key    | ????????? | string | ??? | default = 'sort_key'
    sort_type    | ???????????? | string | ??? | default = 'ASC'
    """

    client = APIClient(request.app, MgrContent)

    api_response = await client.retrieve(
        opt_id=None,
        condition={
            "product_type": product_type.value if product_type
                                                  is not None else None,
            "content_type": content_type.value if content_type
                                                  is not None else None,
            "content_name": content_name,
            "publisher": publisher,
            "status": status.value if status is not None else None,
            "release_manager": release_manager,
            "release_date_from": release_date_from,
            "release_date_to": release_date_to,
            "cancel_date_from": cancel_date_from,
            "cancel_date_to": cancel_date_to
        },
        extra_params={
            "page": page,
            "per_page": int(per_page),
            "sort_key": sort_key.value if sort_key is not None else None,
            "sort_type": sort_type,
        },
        paging_model=PagedContent,
    )

    response = PagedContent()
    detail = getattr(api_response, 'detail', 0)
    response_model = MgrContent.parse_obj(
        {
            "page": page,
            "has_next": page * int(per_page) < detail['count'],
            "total_pages": math.ceil(detail['count'] / int(per_page)),
            "contents": detail['contents'],
            "count": detail['count'],
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
