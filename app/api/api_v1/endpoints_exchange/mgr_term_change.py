"""管理员term修改"""

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
from app.schemas.mgr_term_change import MgrTermChangeIn, \
    MgrTermChangeOut

router = APIRouter()


@router.put(
    "/terms/tag/{term_id}",
    response_model=MgrTermChangeOut,
    responses=dict([
        ResponseSchema(sc.OK, MgrTermChangeOut),
        ResponseErrorSchema(sc.BAD_REQUEST, tc.PARAM_ENTRY_101_ERROR),
        ResponseErrorSchema(sc.UNAUTHORIZED, tc.INVALID_USER_SESSION_106),
        ResponseErrorSchema(sc.FORBIDDEN, tc.AUTH_108_ERROR),
        ResponseErrorSchema(sc.NOT_FOUND, tc.DATA_NOT_FOUND_109),
    ])
)
async def manager_term_change(
        request: Request,
        term_id: str = Path(..., 
                            title="termID", 
                            max_length=100,
                            regex=r"^[_0-9a-z]*$",
                            ),
        term_type: EnumTermType = Query(default=EnumTermType.tag,
                                        title="term类型"),
        request_body_params: MgrTermChangeIn = None,
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
    slug|slug|string|body|是|
    text|term文本|string|body|是|
    description|描述|string|body|是|
    sort_key|排序键|string|body|否|
    product_type|产品类别|string|body|否|`['any_share_cloud','any_backup_cloud','any_robot_cloud']`
    content_type|类容分类|string|body|否|`['application','solution','service']`
    """

    client = APIClient(request.app, MgrTermChangeOut)
    api_response = await client.update(
        opt_id={**request_body_params.dict()},
        obj_in={
            **request_body_params.dict(),
            "term_id": term_id,
            "term_type": term_type.value if term_type else None,
        }
    )
    logger.info("管理员term修改")
    return JSONResponse(status_code=sc.OK,
                        content=api_response.dict(),
                        headers={'x-onetimetoken': await onetimetoken_reset(
                            request, access_token)},
                        )


@router.put(
    "/terms/group/{term_id}",
    response_model=MgrTermChangeOut,
    responses=dict([
        ResponseSchema(sc.OK, MgrTermChangeOut),
        ResponseErrorSchema(sc.BAD_REQUEST, tc.PARAM_ENTRY_101_ERROR),
        ResponseErrorSchema(sc.UNAUTHORIZED, tc.INVALID_USER_SESSION_106),
        ResponseErrorSchema(sc.FORBIDDEN, tc.AUTH_108_ERROR),
        ResponseErrorSchema(sc.NOT_FOUND, tc.DATA_NOT_FOUND_109),
    ])
)
async def alias_manager_term_change_group(
        request: Request,
        access_token: str = Depends(get_exchange_user),
        request_body_params: MgrTermChangeIn = None,
        term_type: EnumTermType = Query(default=EnumTermType.group,
                                        title="term类型"),
        term_id: str = Path(..., 
                            title="termID",
                            max_length=100,
                            regex=r"^[_0-9a-z]*$",
                            ),
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
    slug|slug|string|body|是|
    text|term文本|string|body|是|
    description|描述|string|body|是|
    sort_key|排序键|string|body|否|
    product_type|产品类别|string|body|否|`['any_share_cloud','any_backup_cloud','any_robot_cloud']`
    content_type|类容分类|string|body|否|`['application','solution','service']`
    """
    return await manager_term_change(
        request=request,
        request_body_params=request_body_params,
        term_type=term_type,
        term_id=term_id,
        access_token=access_token,
    )
