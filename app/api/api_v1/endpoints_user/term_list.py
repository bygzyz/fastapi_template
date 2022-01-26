import math
from pydantic import PositiveInt
from typing import Optional
from fastapi import APIRouter, Query, Path, Request
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.core.constants import EnumTermType, EnumManagerPerPage, \
    EnumUserPerPage, EnumSortKeyUserTerms
from app.schemas.terms import Term, PagedTerm
from app.core._responses import ResponseErrorSchema
from app.core._status_code import status_codes as sc, \
    trace_codes as tc
from app.rpc.async_http_client import APIClient

router = APIRouter()


@router.get(
    "/terms/{term_type}",
    response_model=Term,
    responses=dict([
        ResponseErrorSchema(sc.BAD_REQUEST, tc.PARAM_ENTRY_101_ERROR),
        ResponseErrorSchema(sc.INTERNAL_SERVER_ERROR,
                            tc.INTERNAL_SERVER_112_ERROR)
    ])
)
async def user_tags_get(
        request: Request,
        term_type: EnumTermType = Path(...,  title="term类型"),
        product_type: str = Query(None, title="产品类型"),
        content_type: str = Query(None, title="内容类型"),
        slug: Optional[str] =
        Query(None, max_length=100, description="",
              regex=r"^[-\w\s\u4E00-\u9FA5\uF900-\uFA2D]*$"),
        text: Optional[str] =
        Query(None, description="", max_length=100,
              regex=r"^[-\w\s\u4E00-\u9FA5\uF900-\uFA2D]*$"),
        page: Optional[int] = Query(settings.PAGE, description="", ge=1,
                                    le=settings.MAX_PAGE),
        per_page: EnumUserPerPage = Query(EnumUserPerPage.ten,
                                          description=""),

        sort_key: Optional[EnumSortKeyUserTerms] =
        Query(EnumSortKeyUserTerms.sort_key, description="",),
        sort_type: Optional[str] = Query("ASC", description="desc or asc"),
                        ):
    """
    # Description
    term一览检索API

    ## Parameter 说明

    参数名 | 参数说明 | 参数类型 | 是否必须 |备注
    -|-|-|-|-
    term_type | term类型   | string | 是 | [tag, group]
    product_type | 产品类型   | string | 否 | 【any_share, any_backup, any_robot】
    content_type | 内容类型   | string | 否 | 【application, solution, service】
    slug    | slug | string | 否 |
    text    | term文本 | string | 否 |
    page    | 第几页  | int | 否 |
    per_page| 每页数目 | int | 否 |

    """

    client = APIClient(request.app, Term)

    api_response = await client.retrieve(
        opt_id=None,
        condition={
            "product_type": product_type,
            "content_type": content_type,
            "term_type": term_type.value,
            "slug": slug,
            "text": text,
        },
        extra_params={
            "page": page,
            "per_page": int(per_page),
            "sort_key": sort_key.value if sort_key is not None else None,
            "sort_type": sort_type,
        },
        paging_model=PagedTerm,
    )

    response = PagedTerm()
    detail = getattr(api_response, "detail", {})
    response_model = Term.parse_obj(
        {
            "term_type": term_type.value,
            "page": page,
            "count": detail['count'],
            "has_next": page * int(per_page) < detail['count'],
            "total_pages": math.ceil(detail['count'] / int(per_page)),
            "terms": detail['terms'],
        }
    )
    response.code = tc.SUCCESS
    response.message = tc.get_reason_phrase(tc.SUCCESS)
    response.detail = response_model.dict()
    return JSONResponse(status_code=sc.OK,
                        content=response.dict())
