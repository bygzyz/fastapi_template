"""管理员内容新增"""

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse

from app.core.esayAuth import get_exchange_user, \
    onetimetoken_reset
from app.core.logger import logger
from app.core.uuid import get_uuid_no_hyphen
from app.core._responses import ResponseSchema, \
    ResponseErrorSchema
from app.core._status_code import status_codes as sc, \
    trace_codes as tc
from app.rpc.async_http_client import APIClient
from app.schemas.mgr_content_add import MgrContentAddFinalOut

router = APIRouter()


@router.post(
    "/contents",
    response_model=MgrContentAddFinalOut,
    responses=dict([
        ResponseSchema(sc.OK, MgrContentAddFinalOut),
        ResponseErrorSchema(sc.BAD_REQUEST, tc.VALIDATION_102_ERROR),
        ResponseErrorSchema(sc.UNAUTHORIZED, tc.INVALID_USER_SESSION_106),
        ResponseErrorSchema(sc.FORBIDDEN, tc.AUTH_108_ERROR),
        ResponseErrorSchema(sc.NOT_FOUND, tc.DATA_NOT_FOUND_109),
    ])
)
async def mgr_content_add(
        request: Request,
        access_token: str = Depends(get_exchange_user)
):
    """
    # Description
    管理员内容新增

    ## 参数说明
    参数名|参数说明|参数类型|参数位置|是否必须|备注|
    -|-|-|-|-|-
    x-AccessToken|认证token|string|header|是
    x-OnetimeToken|一次认证token|string|header|是
    x-Userid|用户id|string|header|是
    x-ClientId|clientId|string|header|否
    X-Forwarded-For|ip|string|header|否
    """

    client = APIClient(request.app, MgrContentAddFinalOut)
    api_response = await client.create(
        obj_in={
            'content_id': get_uuid_no_hyphen(),
            'record_id': get_uuid_no_hyphen(),
        }
    )
    logger.info("管理员内容新增")
    return JSONResponse(status_code=sc.OK,
                        content=api_response.dict(),
                        headers={'x-onetimetoken': await onetimetoken_reset(
                            request, access_token)},
                        )
