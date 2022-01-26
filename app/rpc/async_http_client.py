import sys

from omi_async_http_client import APIClient as omi_api_client_builder
from omi_async_http_client import AioHttpClientBackend
from omi_async_http_client import api_request_model
from app.core.config import settings

# sys.path.append("../../")


def rpc_api_client_builder(app, model):
    # from bootstrap import app

    return omi_api_client_builder(
        model=model,
        app=app,
        http_backend=settings.HTTP_BACKEND,
        resource_endpoint=settings.RESOURCE_ENDPOINT,
        client_id=settings.CLIENT_ID,
        client_secret=settings.CLIENT_SECRET
    )


APIClient = rpc_api_client_builder
