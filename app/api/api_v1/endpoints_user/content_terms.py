"""内容term检索"""

from fastapi import APIRouter, status, Query, Path, Request
from fastapi.responses import JSONResponse

from app.core.constants import EnumTermType
from app.core.logger import logger
from app.core._responses import ResponseSchema, \
    ResponseErrorSchema
from app.core._status_code import status_codes as sc, \
    trace_codes as tc
from app.rpc.async_http_client import APIClient
from app.schemas.content_terms import ContentTermsFinalOut

router = APIRouter()


@router.get(
    "/contents/terms/tag/{record_id}",
    response_model=ContentTermsFinalOut,
    responses=dict([
        ResponseSchema(sc.OK, ContentTermsFinalOut),
        ResponseErrorSchema(sc.BAD_REQUEST, tc.PARAM_ENTRY_101_ERROR)
    ])
)
async def content_terms(
        request: Request,
        record_id: str = Path(...,
                              title="记录ID",
                              max_length=100,
                              regex=r"^[_0-9a-z]*$",
                              ),
        term_type: EnumTermType = Query(default=EnumTermType.tag,
                                        title="term类型",
                                        )
):
    """
    # Description
    内容term检索

    ## 参数说明
    参数名|参数说明|参数类型|参数位置|是否必须|备注|
    -|-|-|-|-|-
    record_id|记录ID|string|query|是|
    term_type|term类型|string|query|是|`['tag','group']`
    """
    client = APIClient(request.app, ContentTermsFinalOut)
    api_response = await client.retrieve(
        opt_id={"record_id": record_id,
                "term_type": term_type.value if term_type else None,
                },
        extra_params={},
    )
    logger.info("用户内容term检索")
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=api_response.dict(),
                        )


@router.get(
    "/contents/terms/group/{record_id}",
    response_model=ContentTermsFinalOut,
    responses=dict([
        ResponseSchema(sc.OK, ContentTermsFinalOut),
        ResponseErrorSchema(sc.BAD_REQUEST, tc.PARAM_ENTRY_101_ERROR),
    ])
)
async def alias_content_terms_group(
        request: Request,
        record_id: str = Path(...,
                              title="记录ID",
                              max_length=100,
                              regex=r"^[_0-9a-z]*$",
                              ),
        term_type: EnumTermType = Query(default=EnumTermType.group,
                                        title="term类型",
                                        ),
):
    """
    # Description
    内容term检索

    ## 参数说明
    参数名|参数说明|参数类型|参数位置|是否必须|备注|
    -|-|-|-|-|-
    record_id|记录ID|string|query|是|
    term_type|term类型|string|query|是|`['tag','group']`
    """
    return await content_terms(
        request=request,
        record_id=record_id,
        term_type=term_type,
    )
