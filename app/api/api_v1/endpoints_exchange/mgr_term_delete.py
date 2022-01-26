"""管理员term删除"""

from fastapi import APIRouter, Depends, Path, Query, Request
from fastapi.responses import JSONResponse

from app.core.constants import EnumTermType
from app.core.esayAuth import get_exchange_user, \
    onetimetoken_reset
from app.core.logger import logger
from app.core._responses import ResponseSchema, \
    ResponseErrorSchema
from app.core._status_code import status_codes as sc, \
    trace_codes as tc
from app.rpc.async_http_client import APIClient
from app.schemas.mgr_term_delete import MgrTermDeleteOut

router = APIRouter()


@router.delete(
    "/terms/tag/{term_id}",
    response_model=MgrTermDeleteOut,
    responses=dict([
        ResponseSchema(sc.OK, MgrTermDeleteOut),
        ResponseErrorSchema(sc.BAD_REQUEST, tc.PARAM_ENTRY_101_ERROR),
        ResponseErrorSchema(sc.UNAUTHORIZED, tc.INVALID_USER_SESSION_106),
        ResponseErrorSchema(sc.FORBIDDEN, tc.AUTH_108_ERROR),
        ResponseErrorSchema(sc.NOT_FOUND, tc.DATA_NOT_FOUND_109),
    ])
)
async def manager_term_delete(
        request: Request,
        term_id: str = Path(...,
                            title="termID",
                            max_length=100,
                            regex=r"^[_0-9a-z]*$",
                            ),
        term_type: EnumTermType = Query(default=EnumTermType.tag,
                                        title="term类型"),
        access_token: str = Depends(get_exchange_user),
):
    """
    # Description
    管理员term删除

    ## 参数说明
    参数名|参数说明|参数类型|参数位置|是否必须|备注|
    -|-|-|-|-|-
    term_id|TermID|string|query|是|
    term_type|term类型|string|query|是|`['tag','group']`
    x-AccessToken|认证token|string|header|是
    x-OnetimeToken|一次认证token|string|header|是
    x-Userid|用户id|string|header|是
    x-ClientId|clientId|string|header|否
    X-Forwarded-For|ip|string|header|否
    """

    client = APIClient(request.app, MgrTermDeleteOut)
    api_response = await client.delete(
        opt_id={
            'term_id': term_id,
            'term_type': term_type.value if term_type else None,
        },
        extra_params={
        }
    )
    logger.info("管理员term删除")
    return JSONResponse(status_code=sc.OK,
                        content=api_response.dict(),
                        headers={'x-onetimetoken': await onetimetoken_reset(
                            request, access_token)},
                        )


@router.delete(
    "/terms/group/{term_id}",
    response_model=MgrTermDeleteOut,
    responses=dict([
        ResponseSchema(sc.OK, MgrTermDeleteOut),
        ResponseErrorSchema(sc.BAD_REQUEST, tc.PARAM_ENTRY_101_ERROR),
        ResponseErrorSchema(sc.UNAUTHORIZED, tc.INVALID_USER_SESSION_106),
        ResponseErrorSchema(sc.FORBIDDEN, tc.AUTH_108_ERROR),
        ResponseErrorSchema(sc.NOT_FOUND, tc.DATA_NOT_FOUND_109),
    ])
)
async def alias_manager_term_delete_group(
        request: Request,
        term_id: str = Path(...,
                            title="termID",
                            max_length=100,
                            regex=r"^[_0-9a-z]*$",
                            ),
        term_type: EnumTermType = Query(default=EnumTermType.group,
                                        title="term类型"),
        access_token: str = Depends(get_exchange_user),
):
    """
    # Description
    管理员term修改

    ## 参数说明
    参数名|参数说明|参数类型|参数位置|是否必须|备注|
    -|-|-|-|-|-
    term_id|TermID|string|query|是|
    term_type|term类型|string|query|是|`['tag','group']`
    x-AccessToken|认证token|string|header|是
    x-OnetimeToken|一次认证token|string|header|是
    x-Userid|用户id|string|header|是
    x-ClientId|clientId|string|header|否
    X-Forwarded-For|ip|string|header|否
    """
    return await manager_term_delete(
        request=request,
        term_type=term_type,
        term_id=term_id,
        access_token=access_token,
    )
