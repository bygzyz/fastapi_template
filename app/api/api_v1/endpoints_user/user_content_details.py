"""用户内容详细检索"""

from fastapi import APIRouter, Path, Request
from fastapi.responses import JSONResponse

from app.core.logger import logger
from app.core._responses import ResponseSchema, ResponseErrorSchema
from app.core._status_code import status_codes as sc, trace_codes as tc
from app.rpc.async_http_client import APIClient
from app.schemas.user_content_details import UserContentDetailsFinalOut

router = APIRouter()


@router.get(
    '/contents/{content_id}',
    response_model=UserContentDetailsFinalOut,
    responses=dict([
        ResponseSchema(sc.OK, UserContentDetailsFinalOut),
        ResponseErrorSchema(sc.BAD_REQUEST, tc.PARAM_ENTRY_101_ERROR),
        ResponseErrorSchema(sc.NOT_FOUND, tc.DATA_NOT_FOUND_109),
    ])
)
async def user_contents_details(
        request: Request,
        content_id: str = Path(...,
                               title="内容ID",
                               max_length=100,
                               regex=r"^[_0-9a-z]*$",
                               ),
):
    """
    # Description
    用户内容详细检索

    ## 参数说明
    参数名|参数说明|参数类型|参数位置|是否必须|备注|
    -|-|-|-|-|-
    content_id|内容ID|string|query|是|
    """
    client = APIClient(request.app, UserContentDetailsFinalOut)
    api_response = await client.retrieve(
        opt_id={"content_id": content_id},
        extra_params={},
    )
    logger.info("用户内容详细检索")
    return JSONResponse(status_code=sc.OK,
                        content=api_response.dict(),
                        )
