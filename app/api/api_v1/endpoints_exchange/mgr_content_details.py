from fastapi import APIRouter, Path, Depends, Request
from fastapi.responses import JSONResponse

from app.core.constants import EnumRecordType
from app.core.esayAuth import get_exchange_user, \
    onetimetoken_reset
from app.schemas.contents_details import ContentDetailModel, \
    ContentDetailResponseModel
from app.core._status_code import status_codes as sc, \
    trace_codes as tc
from app.core._responses import ResponseErrorSchema
from app.rpc.async_http_client import APIClient

router = APIRouter()


@router.get("/contents/manager/{record_type}/{record_id}",
            response_model=ContentDetailModel,
            responses=dict([
                ResponseErrorSchema(sc.BAD_REQUEST, tc.PARAM_ENTRY_101_ERROR),
                ResponseErrorSchema(sc.NOT_FOUND, tc.DATA_NOT_FOUND_109),
                ResponseErrorSchema(sc.UNAUTHORIZED,
                                    tc.INVALID_USER_SESSION_106),
                ResponseErrorSchema(sc.FORBIDDEN, tc.AUTH_108_ERROR),
                ResponseErrorSchema(sc.INTERNAL_SERVER_ERROR,
                                    tc.INTERNAL_SERVER_112_ERROR)

            ]))
async def manager_content_details(
        request: Request,
        access_token: str = Depends(get_exchange_user),
        record_type: EnumRecordType = Path(..., description=""),
        record_id: str = Path(..., description="", max_length=100,
                              min_length=1, regex=r"^[0-9a-z_]*$"),
):
    """

    # Description
    管理员内容详细检索

    ## parameter 说明
    参数名 | 参数说明 | 参数类型 | 是否必须 |备注
    -|-|-|-|-
    record_type | 记录类型 | string | 是 | 【draft, publish, inherit】
    record_id | 记录ID | string | 是 |

    """

    client = APIClient(request.app, ContentDetailResponseModel)

    api_response = await client.retrieve(
        opt_id={"record_id": record_id},
        condition={
            "record_id": record_id,
            "record_type": record_type.value,
        },
        extra_params={},
    )
    api_response.code = tc.SUCCESS
    api_response.message = tc.get_reason_phrase(tc.SUCCESS)

    return JSONResponse(
        status_code=sc.OK,
        content=api_response.dict(),
        headers={
            "x-onetimeToken": await onetimetoken_reset(request, access_token)}
    )
