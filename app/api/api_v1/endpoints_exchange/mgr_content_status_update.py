import json
from fastapi import APIRouter, status as s, Path, Depends, Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from app.schemas.mgr_content_status_update import \
    MgrContentStatusUpdateResponse, MgrStatusUpdate
from app.core.config import settings
from app.core.error import PARAM_ENTRY_101_ERROR, \
    PARAM_ENTRY_101_ERROR_MESSAGE
from app.core._status_code import status_codes as sc, \
    trace_codes as tc
from app.core._responses import ResponseErrorSchema
from app.rpc.async_http_client import APIClient
from app.core.esayAuth import get_exchange_user, \
    onetimetoken_reset

router = APIRouter()


@router.put("/contents/publish/{content_id}",
            response_model=MgrContentStatusUpdateResponse,
            responses=dict([
                ResponseErrorSchema(sc.BAD_REQUEST, tc.PARAM_ENTRY_101_ERROR),
                ResponseErrorSchema(sc.NOT_FOUND, tc.DATA_NOT_FOUND_109),
                ResponseErrorSchema(sc.UNAUTHORIZED,
                                    tc.INVALID_USER_SESSION_106),
                ResponseErrorSchema(sc.FORBIDDEN, tc.AUTH_108_ERROR),
                ResponseErrorSchema(sc.CONFLICT, tc.DATA_ALREADY_MODIFIED_110),
                ResponseErrorSchema(sc.INTERNAL_SERVER_ERROR,
                                    tc.INTERNAL_SERVER_112_ERROR)

            ])
            )
async def manager_update_status(
        request: Request,
        params: MgrStatusUpdate,
        content_id: str = Path(..., title="内容ID", max_length=100,
                               min_length=1, description="",
                               regex=r"^[0-9a-z_]*$"),
        access_token: str = Depends(get_exchange_user),
):
    """

    # Description
    管理员内容状态更新

    ## Parameter 说明
    参数名 | 参数说明 | 参数类型 | 是否必须 |备注
    -|-|-|-|-
    content_id   | 内容ID       | string | 是 |
    status       | 数据库现存状态 | string | 是 | 【init, release, stop】
    update_status| 更新的状态    | string | 是 | 【init, release, stop】

    """
    redis = request.app.state.OMI_CACHE_MANAGER
    access_key = (settings.REDIS_PREFIX +
                  settings.REDIS_DOMAIN_ACCESS_TOKEN +
                  settings.ACCESSTOKEN_PREFIX + access_token)
    access_redis = await redis.get(access_key)
    access_redis = json.loads(access_redis)
    user_id_short = access_redis.get("user_id_short")

    params = jsonable_encoder(params)
    status = params["status"]
    update_status = params["update_status"]

    # 判断status是否在指定类型中 以及当前状态与将要更新为的状态是否相等
    if status == update_status:
        return JSONResponse(status_code=s.HTTP_400_BAD_REQUEST,
                            content={"code": PARAM_ENTRY_101_ERROR,
                                     "message": PARAM_ENTRY_101_ERROR_MESSAGE,
                                     "detail": {}})

    # 编辑请求参数,以dict创建status_update,键conditions 为检索条件, 键 value为更新值
    status_update = dict()
    conditions = dict()
    # 检索条件为content_id 和status
    conditions["content_id"] = content_id
    conditions["status"] = status
    status_update["conditions"] = conditions
    value = dict()
    value["status"] = update_status
    # 如果更新为下架， 则同时更新 下架人 下架时间
    if update_status == "cancel":
        value["manager"] = user_id_short
        status_update["value"] = value

    else:
        # 如果更新为上传，则设置cancel_date 和 cancel_manager为空
        value["cancel_date"] = None
        # 更新上传者和上传时间 取当前用户和当前时间
        value["manager"] = user_id_short
        status_update["value"] = value

    client = APIClient(request.app, MgrContentStatusUpdateResponse)

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
