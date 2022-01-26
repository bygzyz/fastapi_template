import json
from fastapi import APIRouter, Path, Depends, Request
from fastapi.responses import JSONResponse
from app.schemas.mgr_content_delete import \
    MgrContentDeleteResponse

from app.core.config import settings
from app.core._responses import ResponseErrorSchema
from app.core._status_code import status_codes as sc, \
    trace_codes as tc
from app.rpc.async_http_client import APIClient
from app.core.esayAuth import get_exchange_user, \
    onetimetoken_reset

router = APIRouter()


@router.delete(
    "/contents/publish/{content_id}",
    response_model=MgrContentDeleteResponse,
    responses=dict([
        ResponseErrorSchema(sc.BAD_REQUEST, tc.PARAM_ENTRY_101_ERROR),
        ResponseErrorSchema(sc.UNAUTHORIZED, tc.INVALID_USER_SESSION_106),
        ResponseErrorSchema(sc.INTERNAL_SERVER_ERROR,
                            tc.INTERNAL_SERVER_112_ERROR)
    ])
)
async def manager_content_delete(
        request: Request,
        access_token: str = Depends(get_exchange_user),
        content_id: str = Path(..., title="内容ID", max_length=100,
                               min_length=1, description="",
                               regex=r"^[0-9a-z_]*$"),
):
    """

    # Description
    管理员内容删除

    ## Parameter 说明

    参数名 | 参数说明 | 参数类型 | 是否必须 |备注
    -|-|-|-|-
    content_id   | 内容ID       | string | 是 |
    """
    # redis = await settings.REDIS.Redis()
    redis = request.app.state.OMI_CACHE_MANAGER
    access_key = (settings.REDIS_PREFIX +
                  settings.REDIS_DOMAIN_ACCESS_TOKEN +
                  settings.ACCESSTOKEN_PREFIX + access_token)
    access_redis = await redis.get(access_key)
    access_redis = json.loads(access_redis)
    user_id_short = access_redis.get("user_id_short")

    # 编辑请求参数，创建字典status_update,键conditions为检索条件， 键value为更新的值
    status_update = dict()
    conditions = dict()
    # 检索条件为当前content_id
    conditions["content_id"] = content_id

    status_update["conditions"] = conditions
    value = dict()
    value["status"] = "cancel"
    # 更新状态为cancel的同时 需要同时更新cancel_date 取当前时间
    # 更新cancel_manager 取当前用户
    value["manager"] = user_id_short
    status_update["value"] = value

    client = APIClient(request.app, MgrContentDeleteResponse)

    api_response = await client.update(
        opt_id={"content_id": content_id},
        obj_in=status_update,
        extra_params={}

    )

    return JSONResponse(
        status_code=sc.OK,
        content=api_response.dict(),
        headers={
            "x-onetimeToken": await onetimetoken_reset(request, access_token)}
    )
