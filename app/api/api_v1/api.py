"""路由"""

from fastapi import APIRouter

from app.api.api_v1.endpoints_user import (
    content_terms,
    user_content_details,
    user_contents,
)

from app.api.api_v1.mock_endpoints import mock_endpoints, \
    auth_fake_endpoint
from app.core.config import settings

api_router = APIRouter()

# ===========================================================
# 用户内容
api_router.include_router(content_terms.router, tags=["User.content"])
api_router.include_router(user_content_details.router, tags=["User.content"])
api_router.include_router(user_contents.router, tags=["User.content"])

# 需要通过api的方式依赖认证 单测专用 什么时候开放请自行控制
api_router.include_router(auth_fake_endpoint.router,
                          tags=["fake_auth_endpoint"])

if settings.USE_MOCK:
    # 单体测试mock路由入口
    api_router.include_router(mock_endpoints.router, tags=["mock_db"])
