"""管理员term新增"""

from fastapi import APIRouter, Query, Depends, Request
from fastapi.responses import JSONResponse

from app.core.constants import EnumTermType
from app.core.esayAuth import get_exchange_user, \
    onetimetoken_reset
from app.core.logger import logger
from app.core.uuid import get_uuid_no_hyphen
from app.core._responses import ResponseSchema, \
    ResponseErrorSchema
from app.core._status_code import status_codes as sc, \
    trace_codes as tc
from app.rpc.async_http_client import APIClient
from app.schemas.mgr_term_add import ManagerTermAddIn, \
    ManagerTermAddOut

router = APIRouter()


@router.post(
    "/terms/tag",
    response_model=ManagerTermAddOut,
    responses=dict([
        ResponseSchema(sc.OK, ManagerTermAddOut),
        ResponseErrorSchema(sc.UNAUTHORIZED, tc.INVALID_USER_SESSION_106),
        ResponseErrorSchema(sc.FORBIDDEN, tc.AUTH_108_ERROR),
        ResponseErrorSchema(sc.CONFLICT, tc.INVALID_USER_SESSION_106),
    ])
)
async def manager_term_add(
        request: Request,
        request_body_params: ManagerTermAddIn,
        term_type: EnumTermType = Query(default=EnumTermType.tag,
                                        title="term类型"),
        access_token: str = Depends(get_exchange_user),
):
    """
    # Description
    管理员term新建

    ## 参数说明
    参数名|参数说明|参数类型|参数位置|是否必须|备注|
    -|-|-|-|-|-
    term_type|term类型|string|query|是|
    x-AccessToken|认证token|string|header|是
    x-OnetimeToken|一次认证token|string|header|是
    x-Userid|用户id|string|header|是
    x-ClientId|clientId|string|header|否
    X-Forwarded-For|ip|string|header|否
    slug|slug|string|body|是|
    text|term文本|string|body|是|
    sort_key|排序键|int|body|否|默认为0
    description|描述|string|body|是|
    product_type|产品类别|string|body|否|`['any_share_cloud','any_backup_cloud','any_robot_cloud']`
    content_type|类容分类|string|body|否|`['application','solution','service']`
    """

    client = APIClient(request.app, ManagerTermAddOut)
    api_response = await client.create(
        obj_in={
            **request_body_params.dict(),
            "term_id": get_uuid_no_hyphen(),
            "term_type": term_type.value if term_type else None,
            "delete_flg": 0,
        }
    )
    logger.info("管理员term新建")
    return JSONResponse(status_code=sc.OK,
                        content=api_response.dict(),
                        headers={'x-onetimetoken': await onetimetoken_reset(
                            request, access_token)},
                        )


@router.post(
    "/terms/group",
    response_model=ManagerTermAddOut,
    responses=dict([
        ResponseSchema(sc.OK, ManagerTermAddOut),
        ResponseErrorSchema(sc.UNAUTHORIZED, tc.INVALID_USER_SESSION_106),
        ResponseErrorSchema(sc.FORBIDDEN, tc.AUTH_108_ERROR),
        ResponseErrorSchema(sc.CONFLICT, tc.INVALID_USER_SESSION_106),
    ])
)
async def alias_manager_term_add_group(
        request: Request,
        request_body_params: ManagerTermAddIn,
        term_type: EnumTermType = Query(default=EnumTermType.group,
                                        title="term类型"),
        access_token: str = Depends(get_exchange_user),
):
    """
    # Description
    管理员term新建

    ## 参数说明
    参数名|参数说明|参数类型|参数位置|是否必须|备注|
    -|-|-|-|-|-
    term_type|term类型|string|query|是|
    x-AccessToken|认证token|string|header|是
    x-OnetimeToken|一次认证token|string|header|是
    x-Userid|用户id|string|header|是
    x-ClientId|clientId|string|header|否
    X-Forwarded-For|ip|string|header|否
    slug|slug|string|body|是|
    text|term文本|string|body|是|
    sort_key|排序键|int|body|否|默认为0
    description|描述|string|body|是|
    product_type|产品类别|string|body|否|`['any_share_cloud','any_backup_cloud','any_robot_cloud']`
    content_type|类容分类|string|body|否|`['application','solution','service']`
    """
    return await manager_term_add(
        request=request,
        request_body_params=request_body_params,
        term_type=term_type,
        access_token=access_token,
    )
