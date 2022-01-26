import json
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, Request
from fastapi.encoders import jsonable_encoder

from app.schemas.contents_details import \
    ContentsDetailsCreate, Simple
from app.schemas.mgr_content_release import \
    MgrContentReleaseResponse
from app.core._responses import ResponseErrorSchema
from app.core._status_code import status_codes as sc, \
    trace_codes as tc
from app.rpc.async_http_client import APIClient
from app.core.config import settings
from app.core.esayAuth import get_exchange_user, \
    onetimetoken_reset

router = APIRouter()


@router.post(
    "/contents/publish",
    response_model=Simple,
    responses=dict([
        ResponseErrorSchema(sc.CONFLICT, tc.DATA_ALREADY_EXIST_111),
        ResponseErrorSchema(sc.UNAUTHORIZED, tc.INVALID_USER_SESSION_106),
        ResponseErrorSchema(sc.BAD_REQUEST, tc.PARAM_ENTRY_101_ERROR),
        ResponseErrorSchema(sc.FORBIDDEN, tc.AUTH_108_ERROR),
        ResponseErrorSchema(sc.INTERNAL_SERVER_ERROR,
                            tc.INTERNAL_SERVER_112_ERROR)
    ])
)
async def manager_release(
        request: Request,
        params: ContentsDetailsCreate,
        access_token: str = Depends(get_exchange_user)
):
    """

    # Description
    管理员发布

    ## Parameter 说明

       参数名 | 参数说明 | 参数类型 | 是否必须 |备注
    -|-|-|-|-
    content_id   | 内容ID  | string | 是 |
    old_record_id   | 记录ID  | string | 是 |
    product_type | 产品类别 | string | 是 | 【any_share, any_backup, any_robot】
    content_name | 内容名称 | string | 是 |
    publisher    | 发布者   | string | 是 |
    description  | 描述   | string | 是 |
    content_type | 内容分类 | string | 是 | 【application, solution, service】
    version    | 发布版本   | string | 是 |
    product_info | 详细介绍   | string | 是 |
    logo_url | logo地址 | string | 是 |
    thumbnail_url | 缩略图 | string | 是 |
    preview_media_urls | 预览媒体地址 | dict | 是 |
    support_info | 支持信息 | dict | 是 |
    email        | 邮箱 | emailstr | 是 |
    phone        | 电话号码 | str | 是 |
    file_id_list | 文件id列表 | list | 是 | 列表内部数据类型为字符串
    tag_id_list | 标签id列表| list | 是 | 列表内部数据类型为字符串
    group_id_list | 组别id列表 | list | 是 | 列表内部数据类型为字符串

    """

    redis = request.app.state.OMI_CACHE_MANAGER
    access_key = (settings.REDIS_PREFIX +
                  settings.REDIS_DOMAIN_ACCESS_TOKEN +
                  settings.ACCESSTOKEN_PREFIX + access_token)
    access_redis = await redis.get(access_key)
    access_redis = json.loads(access_redis)
    user_id_short = access_redis.get("user_id_short")
    # 编辑请求参数
    insert_data = jsonable_encoder(params)

    insert_data["user_id_short"] = user_id_short

    # delete_flg 默认为 0
    insert_data["delete_flg"] = 0
    # 记录类型默认为publish
    insert_data["record_type"] = "publish"

    client = APIClient(request.app, MgrContentReleaseResponse)

    api_response = await client.create(
        obj_in=insert_data,
        extra_params={},
    )
    return JSONResponse(
        status_code=sc.OK,
        content=api_response.dict(),
        headers={
            "x-onetimeToken": await onetimetoken_reset(request, access_token)}
    )
